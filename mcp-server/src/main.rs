use rmcp::{
    ServerHandler, ServiceExt,
    handler::server::{router::tool::ToolRouter, wrapper::Parameters},
    model::{Implementation, ProtocolVersion, ServerCapabilities, ServerInfo},
    schemars, tool, tool_handler, tool_router,
    transport::sse_server::SseServer,
};
use serde::Deserialize;
use serde_json::{json, Value};

// ── Parameter structs ─────────────────────────────────────────────────────────

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct ListApplicationsParams {
    /// Filter by status: Pipeline, Applied, Screening, Interview, Offer, Closed
    status: Option<String>,
    /// Filter by priority: P1, P2, P3, P4
    priority: Option<String>,
    /// Maximum number of results to return (default: 50)
    limit: Option<i64>,
    /// Number of results to skip for pagination (default: 0)
    offset: Option<i64>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct AddApplicationParams {
    /// Company name. A new company is created automatically if it doesn't exist.
    company_name: String,
    /// Job role/title
    role: String,
    /// Priority P1 (highest urgency) through P4 (lowest). Defaults to P4.
    priority: Option<String>,
    /// Status: Pipeline, Applied, Screening, Interview, Offer, Closed. Defaults to Pipeline.
    status: Option<String>,
    /// Link to the job posting
    job_url: Option<String>,
    /// Office location
    location: Option<String>,
    /// Remote policy (e.g. "Remote", "Hybrid", "On-site")
    remote_policy: Option<String>,
    /// Salary range (e.g. "$150k-$180k")
    salary_range: Option<String>,
    /// Free-form notes
    notes: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct UpdateApplicationParams {
    /// ID of the application to update
    id: i64,
    /// New status: Pipeline, Applied, Screening, Interview, Offer, Closed
    status: Option<String>,
    /// New priority: P1, P2, P3, P4
    priority: Option<String>,
    /// Job role/title
    role: Option<String>,
    /// Link to the job posting
    job_url: Option<String>,
    /// Office location
    location: Option<String>,
    /// Remote policy (e.g. "Remote", "Hybrid", "On-site")
    remote_policy: Option<String>,
    /// Salary range (e.g. "$150k-$180k")
    salary_range: Option<String>,
    /// Hiring manager's name
    hiring_manager_name: Option<String>,
    /// Hiring manager's email address
    hiring_manager_email: Option<String>,
    /// Date applied (ISO 8601, e.g. 2026-03-20T00:00:00)
    date_applied: Option<String>,
    /// Date screening occurred (ISO 8601)
    date_screening: Option<String>,
    /// Date first interview occurred (ISO 8601)
    date_interview: Option<String>,
    /// Date offer received (ISO 8601)
    date_offer: Option<String>,
    /// Date application was closed (ISO 8601)
    date_closed: Option<String>,
    /// Free-form notes
    notes: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct LogInteractionParams {
    /// ID of the application this interaction belongs to
    application_id: i64,
    /// Type of interaction: email, call, meeting, linkedin, other
    #[serde(rename = "type")]
    interaction_type: String,
    /// Name of the person you interacted with
    contact_person: Option<String>,
    /// What was discussed or decided
    summary: Option<String>,
    /// Follow-up actions required
    next_steps: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct ApplicationIdParams {
    /// Application ID
    application_id: i64,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct CreateOfferParams {
    /// ID of the application this offer belongs to
    application_id: i64,
    /// Base salary in whole dollars (e.g. 200000 for $200k)
    base_salary: Option<i64>,
    /// Annual bonus target in whole dollars
    bonus_target: Option<i64>,
    /// Signing bonus in whole dollars
    signing_bonus: Option<i64>,
    /// Total equity value in whole dollars
    equity_value: Option<i64>,
    /// Equity details (vesting schedule, cliff, etc.)
    equity_details: Option<String>,
    /// Total annual compensation in whole dollars
    total_comp: Option<i64>,
    /// Offer date (ISO 8601, e.g. 2026-03-20T00:00:00)
    offer_date: Option<String>,
    /// Deadline to respond (ISO 8601)
    response_deadline: Option<String>,
    /// PTO days per year
    pto_days: Option<i64>,
    /// Start date (ISO 8601)
    start_date: Option<String>,
    /// Remote policy (e.g. "Remote", "Hybrid", "On-site")
    remote_policy: Option<String>,
    /// Offer status: Pending, Accepted, Declined, Negotiating. Defaults to Pending.
    status: Option<String>,
    /// Free-form notes about the offer
    notes: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct UpdateInterviewParams {
    /// ID of the interview to update
    id: i64,
    /// Mark as completed: "Yes" or "No"
    completed: Option<String>,
    /// Updated date and time (ISO 8601, e.g. 2026-03-25T14:00:00)
    scheduled_date: Option<String>,
    /// Type: phone, video, onsite, technical, behavioral, other
    interview_type: Option<String>,
    /// Name of the interviewer
    interviewer_name: Option<String>,
    /// Email of the interviewer
    interviewer_email: Option<String>,
    /// Title/role of the interviewer
    interviewer_title: Option<String>,
    /// Physical location (for onsite interviews)
    location: Option<String>,
    /// Zoom/Meet/Teams link
    meeting_link: Option<String>,
    /// Notes or debrief
    notes: Option<String>,
}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct ScheduleInterviewParams {
    /// ID of the application this interview is for
    application_id: i64,
    /// Type: phone, video, onsite, technical, behavioral, other
    interview_type: Option<String>,
    /// Date and time (ISO 8601, e.g. 2026-03-25T14:00:00)
    scheduled_date: Option<String>,
    /// Name of the interviewer
    interviewer_name: Option<String>,
    /// Zoom/Meet/Teams link
    meeting_link: Option<String>,
    /// Prep notes or other context
    notes: Option<String>,
}

// ── Server ────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
struct JobTrackerServer {
    tool_router: ToolRouter<Self>,
    client: reqwest::Client,
    base_url: String,
}

// Helper methods (not tools)
impl JobTrackerServer {
    fn new(base_url: String) -> Self {
        Self {
            tool_router: Self::tool_router(),
            client: reqwest::Client::new(),
            base_url,
        }
    }

    async fn api_get(&self, path: &str) -> Result<Value, String> {
        let resp = self.client
            .get(format!("{}{}", self.base_url, path))
            .send()
            .await
            .map_err(|e| e.to_string())?;
        let status = resp.status();
        eprintln!("[mcp] GET {} -> {}", path, status);
        resp.json().await.map_err(|e| e.to_string())
    }

    /// Like api_get but also returns the X-Total-Count header value if present.
    async fn api_get_with_count(&self, path: &str) -> Result<(Value, Option<i64>), String> {
        let resp = self.client
            .get(format!("{}{}", self.base_url, path))
            .send()
            .await
            .map_err(|e| e.to_string())?;
        let status = resp.status();
        eprintln!("[mcp] GET {} -> {}", path, status);
        let total = resp
            .headers()
            .get("x-total-count")
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.parse::<i64>().ok());
        let body = resp.json().await.map_err(|e| e.to_string())?;
        Ok((body, total))
    }

    async fn api_post(&self, path: &str, body: Value) -> Result<Value, String> {
        let resp = self.client
            .post(format!("{}{}", self.base_url, path))
            .json(&body)
            .send()
            .await
            .map_err(|e| e.to_string())?;
        let status = resp.status();
        eprintln!("[mcp] POST {} -> {}", path, status);
        resp.json().await.map_err(|e| e.to_string())
    }

    async fn api_put(&self, path: &str, body: Value) -> Result<Value, String> {
        let resp = self.client
            .put(format!("{}{}", self.base_url, path))
            .json(&body)
            .send()
            .await
            .map_err(|e| e.to_string())?;
        let status = resp.status();
        eprintln!("[mcp] PUT {} -> {}", path, status);
        resp.json().await.map_err(|e| e.to_string())
    }

    /// Look up a company by name, creating it if it doesn't exist.
    async fn find_or_create_company(&self, name: &str) -> Result<i64, String> {
        let companies = self.api_get("/api/companies?limit=500").await?;
        if let Some(arr) = companies.as_array() {
            for c in arr {
                if c["name"].as_str() == Some(name) {
                    return c["id"].as_i64().ok_or_else(|| "Invalid company id".to_string());
                }
            }
        }
        let created = self
            .api_post("/api/companies", json!({ "name": name }))
            .await?;
        created["id"]
            .as_i64()
            .ok_or_else(|| "Invalid company id in response".to_string())
    }
}

// ── Tool definitions ──────────────────────────────────────────────────────────

#[tool_router]
impl JobTrackerServer {
    #[tool(description = "Get dashboard statistics: total applications, breakdown by status and priority, recent activity, and upcoming interviews.")]
    async fn get_dashboard(&self) -> String {
        match self.api_get("/api/dashboard").await {
            Ok(v) => serde_json::to_string_pretty(&v).unwrap_or_else(|e| e.to_string()),
            Err(e) => format!("Error fetching dashboard: {e}"),
        }
    }

    #[tool(description = "List job applications (summary view). Optionally filter by status \
        (Pipeline/Applied/Screening/Interview/Offer/Closed) or priority (P1-P4). \
        Supports pagination via limit (default 50) and offset (default 0). \
        Returns {total, limit, offset, has_more, items}. \
        If has_more is true, call again with offset += limit to fetch the next page. \
        Items omit verbose fields like match_reasoning and notes.")]
    async fn list_applications(
        &self,
        Parameters(ListApplicationsParams { status, priority, limit, offset }): Parameters<ListApplicationsParams>,
    ) -> String {
        let limit = limit.unwrap_or(50);
        let offset = offset.unwrap_or(0);
        let mut path = format!("/api/applications?limit={limit}&skip={offset}");
        if let Some(s) = &status {
            path.push_str(&format!("&status={s}"));
        }
        if let Some(p) = &priority {
            path.push_str(&format!("&priority={p}"));
        }
        match self.api_get_with_count(&path).await {
            Ok((Value::Array(apps), total)) => {
                let items: Vec<Value> = apps
                    .into_iter()
                    .map(|mut a| {
                        for field in &[
                            "match_reasoning", "match_strengths", "match_gaps",
                            "notes", "cover_letter_filename", "resume_filename",
                            "hiring_manager_name", "hiring_manager_email",
                            "created_at", "updated_at",
                        ] {
                            a.as_object_mut().map(|o| o.remove(*field));
                        }
                        a
                    })
                    .collect();
                let count = items.len() as i64;
                let total = total.unwrap_or(count + offset);
                let has_more = offset + count < total;
                let envelope = json!({
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": has_more,
                    "items": items,
                });
                serde_json::to_string(&envelope).unwrap_or_else(|e| e.to_string())
            }
            Ok((v, _)) => serde_json::to_string(&v).unwrap_or_else(|e| e.to_string()),
            Err(e) => format!("Error listing applications: {e}"),
        }
    }

    #[tool(description = "Add a new job application to the tracker. Automatically creates the company if it doesn't exist yet.")]
    async fn add_application(
        &self,
        Parameters(params): Parameters<AddApplicationParams>,
    ) -> String {
        let company_id = match self.find_or_create_company(&params.company_name).await {
            Ok(id) => id,
            Err(e) => {
                return format!("Error finding/creating company '{}': {e}", params.company_name)
            }
        };

        let mut body = json!({ "company_id": company_id, "role": params.role });
        if let Some(v) = params.priority { body["priority"] = json!(v); }
        if let Some(v) = params.status { body["status"] = json!(v); }
        if let Some(v) = params.job_url { body["job_url"] = json!(v); }
        if let Some(v) = params.location { body["location"] = json!(v); }
        if let Some(v) = params.remote_policy { body["remote_policy"] = json!(v); }
        if let Some(v) = params.salary_range { body["salary_range"] = json!(v); }
        if let Some(v) = params.notes { body["notes"] = json!(v); }

        match self.api_post("/api/applications", body).await {
            Ok(v) => format!(
                "Created application #{} — {} at {} (status: {}, priority: {})",
                v["id"].as_i64().unwrap_or(0),
                v["role"].as_str().unwrap_or("unknown"),
                params.company_name,
                v["status"].as_str().unwrap_or("Pipeline"),
                v["priority"].as_str().unwrap_or("P4"),
            ),
            Err(e) => format!("Error creating application: {e}"),
        }
    }

    #[tool(description = "Update an existing application. Supports status, priority, role, job_url, \
        location, remote_policy, salary_range, hiring_manager_name, hiring_manager_email, \
        date_applied, date_screening, date_interview, date_offer, date_closed, and notes.")]
    async fn update_application(
        &self,
        Parameters(params): Parameters<UpdateApplicationParams>,
    ) -> String {
        let id = params.id;
        let mut body = json!({});
        if let Some(v) = params.status               { body["status"] = json!(v); }
        if let Some(v) = params.priority              { body["priority"] = json!(v); }
        if let Some(v) = params.role                  { body["role"] = json!(v); }
        if let Some(v) = params.job_url               { body["job_url"] = json!(v); }
        if let Some(v) = params.location              { body["location"] = json!(v); }
        if let Some(v) = params.remote_policy         { body["remote_policy"] = json!(v); }
        if let Some(v) = params.salary_range          { body["salary_range"] = json!(v); }
        if let Some(v) = params.hiring_manager_name   { body["hiring_manager_name"] = json!(v); }
        if let Some(v) = params.hiring_manager_email  { body["hiring_manager_email"] = json!(v); }
        if let Some(v) = params.date_applied          { body["date_applied"] = json!(v); }
        if let Some(v) = params.date_screening        { body["date_screening"] = json!(v); }
        if let Some(v) = params.date_interview        { body["date_interview"] = json!(v); }
        if let Some(v) = params.date_offer            { body["date_offer"] = json!(v); }
        if let Some(v) = params.date_closed           { body["date_closed"] = json!(v); }
        if let Some(v) = params.notes                 { body["notes"] = json!(v); }

        match self.api_put(&format!("/api/applications/{id}"), body).await {
            Ok(v) => format!(
                "Updated application #{id} — {} at {} → status: {}, priority: {}",
                v["role"].as_str().unwrap_or("?"),
                v.get("company").and_then(|c| c["name"].as_str()).unwrap_or("?"),
                v["status"].as_str().unwrap_or("?"),
                v["priority"].as_str().unwrap_or("?"),
            ),
            Err(e) => format!("Error updating application #{id}: {e}"),
        }
    }

    #[tool(description = "Log an interaction (email, call, meeting, LinkedIn message) against a job application.")]
    async fn log_interaction(
        &self,
        Parameters(params): Parameters<LogInteractionParams>,
    ) -> String {
        let mut body = json!({
            "application_id": params.application_id,
            "type": params.interaction_type,
        });
        if let Some(v) = params.contact_person { body["contact_person"] = json!(v); }
        if let Some(v) = params.summary { body["summary"] = json!(v); }
        if let Some(v) = params.next_steps { body["next_steps"] = json!(v); }

        match self.api_post("/api/interactions", body).await {
            Ok(v) => format!(
                "Logged interaction #{} for application #{}",
                v["id"].as_i64().unwrap_or(0),
                params.application_id
            ),
            Err(e) => format!("Error logging interaction: {e}"),
        }
    }

    #[tool(description = "List all interactions (emails, calls, meetings) recorded for a job application.")]
    async fn list_interactions(
        &self,
        Parameters(ApplicationIdParams { application_id }): Parameters<ApplicationIdParams>,
    ) -> String {
        match self
            .api_get(&format!("/api/applications/{application_id}/interactions"))
            .await
        {
            Ok(v) => serde_json::to_string_pretty(&v).unwrap_or_else(|e| e.to_string()),
            Err(e) => format!("Error listing interactions: {e}"),
        }
    }

    #[tool(description = "Schedule an interview for a job application.")]
    async fn schedule_interview(
        &self,
        Parameters(params): Parameters<ScheduleInterviewParams>,
    ) -> String {
        let mut body = json!({ "application_id": params.application_id });
        if let Some(v) = params.interview_type { body["interview_type"] = json!(v); }
        if let Some(v) = params.scheduled_date { body["scheduled_date"] = json!(v); }
        if let Some(v) = params.interviewer_name { body["interviewer_name"] = json!(v); }
        if let Some(v) = params.meeting_link { body["meeting_link"] = json!(v); }
        if let Some(v) = params.notes { body["notes"] = json!(v); }

        match self.api_post("/api/interviews", body).await {
            Ok(v) => format!(
                "Scheduled {} interview #{} for application #{}",
                v["interview_type"].as_str().unwrap_or(""),
                v["id"].as_i64().unwrap_or(0),
                params.application_id
            ),
            Err(e) => format!("Error scheduling interview: {e}"),
        }
    }

    #[tool(description = "Get all upcoming interviews from the dashboard.")]
    async fn get_upcoming_interviews(&self) -> String {
        match self.api_get("/api/dashboard").await {
            Ok(v) => serde_json::to_string_pretty(&v["upcoming_interviews"])
                .unwrap_or_else(|e| e.to_string()),
            Err(e) => format!("Error fetching upcoming interviews: {e}"),
        }
    }

    #[tool(description = "Compare all job offers side by side (compensation, benefits, equity, etc.).")]
    async fn compare_offers(&self) -> String {
        match self.api_get("/api/offers/compare/all").await {
            Ok(v) => serde_json::to_string_pretty(&v).unwrap_or_else(|e| e.to_string()),
            Err(e) => format!("Error fetching offer comparison: {e}"),
        }
    }

    #[tool(description = "Record a job offer received for an application. Provide compensation \
        details: base salary, bonus, signing bonus, equity, total comp (all in whole dollars, \
        e.g. 200000 for $200k), plus offer date, response deadline, PTO days, start date, \
        remote policy, and notes.")]
    async fn create_offer(
        &self,
        Parameters(params): Parameters<CreateOfferParams>,
    ) -> String {
        let mut body = json!({ "application_id": params.application_id });
        if let Some(v) = params.base_salary        { body["base_salary"] = json!(v); }
        if let Some(v) = params.bonus_target       { body["bonus_target"] = json!(v); }
        if let Some(v) = params.signing_bonus      { body["signing_bonus"] = json!(v); }
        if let Some(v) = params.equity_value       { body["equity_value"] = json!(v); }
        if let Some(v) = params.equity_details     { body["equity_details"] = json!(v); }
        if let Some(v) = params.total_comp         { body["total_comp"] = json!(v); }
        if let Some(v) = params.offer_date         { body["offer_date"] = json!(v); }
        if let Some(v) = params.response_deadline  { body["response_deadline"] = json!(v); }
        if let Some(v) = params.pto_days           { body["pto_days"] = json!(v); }
        if let Some(v) = params.start_date         { body["start_date"] = json!(v); }
        if let Some(v) = params.remote_policy      { body["remote_policy"] = json!(v); }
        if let Some(v) = params.status             { body["status"] = json!(v); }
        if let Some(v) = params.notes              { body["notes"] = json!(v); }

        match self.api_post("/api/offers", body).await {
            Ok(v) => format!(
                "Created offer #{} for application #{} — base: ${}, total comp: ${}, deadline: {}",
                v["id"].as_i64().unwrap_or(0),
                params.application_id,
                v["base_salary"].as_i64().unwrap_or(0),
                v["total_comp"].as_i64().unwrap_or(0),
                v["response_deadline"].as_str().unwrap_or("not set"),
            ),
            Err(e) => format!("Error creating offer: {e}"),
        }
    }

    #[tool(description = "Update an existing interview. Use this to mark an interview as completed, \
        reschedule it, add debrief notes, or update interviewer details. \
        completed accepts \"Yes\" or \"No\".")]
    async fn update_interview(
        &self,
        Parameters(params): Parameters<UpdateInterviewParams>,
    ) -> String {
        let id = params.id;
        let mut body = json!({});
        if let Some(v) = params.completed          { body["completed"] = json!(v); }
        if let Some(v) = params.scheduled_date     { body["scheduled_date"] = json!(v); }
        if let Some(v) = params.interview_type     { body["interview_type"] = json!(v); }
        if let Some(v) = params.interviewer_name   { body["interviewer_name"] = json!(v); }
        if let Some(v) = params.interviewer_email  { body["interviewer_email"] = json!(v); }
        if let Some(v) = params.interviewer_title  { body["interviewer_title"] = json!(v); }
        if let Some(v) = params.location           { body["location"] = json!(v); }
        if let Some(v) = params.meeting_link       { body["meeting_link"] = json!(v); }
        if let Some(v) = params.notes              { body["notes"] = json!(v); }

        match self.api_put(&format!("/api/interviews/{id}"), body).await {
            Ok(v) => format!(
                "Updated interview #{id} — type: {}, completed: {}, date: {}",
                v["interview_type"].as_str().unwrap_or("?"),
                v["completed"].as_str().unwrap_or("?"),
                v["scheduled_date"].as_str().unwrap_or("not scheduled"),
            ),
            Err(e) => format!("Error updating interview #{id}: {e}"),
        }
    }
}

// ── ServerHandler ─────────────────────────────────────────────────────────────

#[tool_handler]
impl ServerHandler for JobTrackerServer {
    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            protocol_version: ProtocolVersion::V_2024_11_05,
            capabilities: ServerCapabilities::builder().enable_tools().build(),
            server_info: Implementation {
                name: env!("CARGO_PKG_NAME").into(),
                version: env!("CARGO_PKG_VERSION").into(),
                ..Default::default()
            },
            instructions: Some(
                "Job search tracker MCP server. \
                Use these tools to manage your pipeline: add applications, log interactions, \
                schedule interviews, and compare offers — all from the terminal."
                    .into(),
            ),
        }
    }
}

// ── Entry point ───────────────────────────────────────────────────────────────

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let base_url = std::env::var("JOB_TRACKER_URL")
        .unwrap_or_else(|_| "http://localhost:8000".to_string());
    let mcp_port: u16 = std::env::var("MCP_PORT")
        .ok()
        .and_then(|p| p.parse().ok())
        .unwrap_or(3000);

    let bind_addr: std::net::SocketAddr = format!("0.0.0.0:{mcp_port}").parse()?;
    println!("MCP server listening on :{mcp_port}");

    let sse_server = SseServer::serve(bind_addr).await?;
    let ct = sse_server.with_service(move || JobTrackerServer::new(base_url.clone()));
    ct.cancelled().await;
    Ok(())
}
