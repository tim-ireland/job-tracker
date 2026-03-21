use rmcp::{
    ServerHandler, ServiceExt,
    handler::server::{router::tool::ToolRouter, wrapper::Parameters},
    model::{Implementation, ProtocolVersion, ServerCapabilities, ServerInfo},
    schemars, tool, tool_handler, tool_router,
    transport::stdio,
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
    /// New status value
    status: Option<String>,
    /// New priority value
    priority: Option<String>,
    /// Updated notes
    notes: Option<String>,
    /// Date applied (ISO 8601, e.g. 2026-03-20T00:00:00)
    date_applied: Option<String>,
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
        self.client
            .get(format!("{}{}", self.base_url, path))
            .send()
            .await
            .map_err(|e| e.to_string())?
            .json()
            .await
            .map_err(|e| e.to_string())
    }

    async fn api_post(&self, path: &str, body: Value) -> Result<Value, String> {
        self.client
            .post(format!("{}{}", self.base_url, path))
            .json(&body)
            .send()
            .await
            .map_err(|e| e.to_string())?
            .json()
            .await
            .map_err(|e| e.to_string())
    }

    async fn api_put(&self, path: &str, body: Value) -> Result<Value, String> {
        self.client
            .put(format!("{}{}", self.base_url, path))
            .json(&body)
            .send()
            .await
            .map_err(|e| e.to_string())?
            .json()
            .await
            .map_err(|e| e.to_string())
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

    #[tool(description = "List job applications. Optionally filter by status (Pipeline/Applied/Screening/Interview/Offer/Closed) or priority (P1-P4).")]
    async fn list_applications(
        &self,
        Parameters(ListApplicationsParams { status, priority }): Parameters<ListApplicationsParams>,
    ) -> String {
        let mut path = "/api/applications?limit=200".to_string();
        if let Some(s) = status {
            path.push_str(&format!("&status={s}"));
        }
        if let Some(p) = priority {
            path.push_str(&format!("&priority={p}"));
        }
        match self.api_get(&path).await {
            Ok(v) => serde_json::to_string_pretty(&v).unwrap_or_else(|e| e.to_string()),
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

    #[tool(description = "Update an existing application's status, priority, notes, or date_applied.")]
    async fn update_application(
        &self,
        Parameters(UpdateApplicationParams { id, status, priority, notes, date_applied }): Parameters<UpdateApplicationParams>,
    ) -> String {
        let mut body = json!({});
        if let Some(v) = &status { body["status"] = json!(v); }
        if let Some(v) = &priority { body["priority"] = json!(v); }
        if let Some(v) = &notes { body["notes"] = json!(v); }
        if let Some(v) = &date_applied { body["date_applied"] = json!(v); }

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

    let server = JobTrackerServer::new(base_url);
    server.serve(stdio()).await?.waiting().await?;
    Ok(())
}
