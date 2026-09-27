document.addEventListener("DOMContentLoaded", async () => {
    if (!window.OpportunityHubAPI.requireAuth()) return;

    const { listSavedOpportunities, deleteSavedOpportunity } = window.OpportunityHubAPI;
    const savedListEl = document.getElementById("savedList");
    const emptyEl = document.getElementById("savedEmpty");
    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            window.OpportunityHubAPI.clearToken();
            window.location.href = "login.html";
        });
    }

    async function loadSaved() {
        try {
            const items = await listSavedOpportunities();
            if (!items.length) {
                savedListEl.innerHTML = "";
                emptyEl.hidden = false;
                return;
            }
            emptyEl.hidden = true;
            savedListEl.innerHTML = items.map((item) => `
                <article class="opportunity-card">
                    <div class="opportunity-card__top">
                        <div>
                            <h3 class="opportunity-card__title">${window.OpportunityHubAPI.escapeHtml(item.title || "Untitled")}</h3>
                            <p class="opportunity-card__org">${window.OpportunityHubAPI.escapeHtml(item.organization || "Unknown org")}</p>
                        </div>
                        <span class="pill">${window.OpportunityHubAPI.escapeHtml(item.category || "Opportunity")}</span>
                    </div>
                    <div class="opportunity-card__meta">
                        <span>${window.OpportunityHubAPI.escapeHtml(item.mode || "Any")}</span>
                        <span>•</span>
                        <span>${window.OpportunityHubAPI.escapeHtml(item.location || "Remote")}</span>
                        <span>•</span>
                        <span>Deadline: ${window.OpportunityHubAPI.formatDate(item.deadline)}</span>
                    </div>
                    <p class="list-description">${window.OpportunityHubAPI.escapeHtml((item.description || "").slice(0, 120))}${(item.description || "").length > 120 ? "…" : ""}</p>
                    <div class="card-actions">
                        <a class="btn btn-secondary small" href="opportunity.html?id=${item.id}">Open</a>
                        <button class="btn btn-primary small" data-unsave-id="${item.id}">Unsave</button>
                    </div>
                </article>
            `).join("");

            document.querySelectorAll("[data-unsave-id]").forEach((button) => {
                button.addEventListener("click", async () => {
                    try {
                        await deleteSavedOpportunity(button.dataset.unsaveId);
                        await loadSaved();
                    } catch (error) {
                        alert(error.message || "Unable to remove save.");
                    }
                });
            });
        } catch (error) {
            savedListEl.innerHTML = `<div class="empty-state">${window.OpportunityHubAPI.escapeHtml(error.message || "Unable to load saved items.")}</div>`;
            emptyEl.hidden = true;
        }
    }

    await loadSaved();
});

