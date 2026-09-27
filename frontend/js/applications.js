document.addEventListener("DOMContentLoaded", async () => {
    if (!window.OpportunityHubAPI.requireAuth()) return;

    const { listApplications, createApplication } = window.OpportunityHubAPI;
    const listEl = document.getElementById("applicationsList");
    const emptyEl = document.getElementById("applicationsEmpty");
    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            window.OpportunityHubAPI.clearToken();
            window.location.href = "login.html";
        });
    }

    try {
        const applications = await listApplications();
        if (!applications.length) {
            listEl.innerHTML = "";
            emptyEl.hidden = false;
            return;
        }

        emptyEl.hidden = true;
        listEl.innerHTML = applications.map((item) => `
            <article class="opportunity-card application-card">
                <div class="opportunity-card__top">
                    <div>
                        <h3 class="opportunity-card__title">Opportunity #${item.opportunity_id}</h3>
                        <p class="opportunity-card__org">Status: ${window.OpportunityHubAPI.escapeHtml(item.status || "Interested")}</p>
                    </div>
                    <span class="pill">${window.OpportunityHubAPI.escapeHtml(item.status || "Interested")}</span>
                </div>
                <div class="opportunity-card__meta">
                    <span>Updated: ${window.OpportunityHubAPI.formatDate(item.updated_at)}</span>
                </div>
                <p class="list-description">${window.OpportunityHubAPI.escapeHtml(item.note || "No note provided.")}</p>
            </article>
        `).join("");
    } catch (error) {
        listEl.innerHTML = `<div class="empty-state">${window.OpportunityHubAPI.escapeHtml(error.message || "Unable to load applications.")}</div>`;
        emptyEl.hidden = true;
    }
});

