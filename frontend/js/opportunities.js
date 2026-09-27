document.addEventListener("DOMContentLoaded", async () => {
    if (!window.OpportunityHubAPI.requireAuth()) return;

    const { listOpportunities, listSavedOpportunities, saveOpportunity, deleteSavedOpportunity } = window.OpportunityHubAPI;
    const searchInput = document.getElementById("searchInput");
    const categorySelect = document.getElementById("categoryFilter");
    const modeSelect = document.getElementById("modeFilter");
    const resultsEl = document.getElementById("opportunitiesResults");
    const emptyEl = document.getElementById("emptyState");
    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            window.OpportunityHubAPI.clearToken();
            window.location.href = "login.html";
        });
    }

    let savedIds = new Set();

    async function refreshSavedIds() {
        try {
            const saved = await listSavedOpportunities();
            savedIds = new Set(saved.map((item) => Number(item.id)));
        } catch (error) {
            savedIds = new Set();
        }
    }

    async function renderOpportunities() {
        const params = {
            search: searchInput.value.trim(),
            category: categorySelect.value || "",
            mode: modeSelect.value || "",
            deadline: "",
        };

        resultsEl.innerHTML = "<div class=\'empty-state\'>Loading opportunities…</div>";
        emptyEl.hidden = true;

        try {
            await refreshSavedIds();
            const opportunities = await listOpportunities(params);
            if (!opportunities.length) {
                resultsEl.innerHTML = "";
                emptyEl.hidden = false;
                return;
            }

            resultsEl.innerHTML = opportunities.map((item) => {
                const isSaved = savedIds.has(Number(item.id));
                const saveLabel = isSaved ? "Saved" : "Save";
                const saveClass = isSaved ? "btn btn-primary small disabled" : "btn btn-secondary small";
                return `
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
                        <p class="list-description">${window.OpportunityHubAPI.escapeHtml((item.description || "").slice(0, 130))}${(item.description || "").length > 130 ? "…" : ""}</p>
                        <div class="card-actions">
                            <a class="btn btn-secondary small" href="opportunity.html?id=${item.id}">View details</a>
                            <button class="${saveClass}" data-save-id="${item.id}" ${isSaved ? "disabled" : ""}>${saveLabel}</button>
                        </div>
                    </article>
                `;
            }).join("");

            document.querySelectorAll("[data-save-id]").forEach((button) => {
                button.addEventListener("click", async () => {
                    const id = button.dataset.saveId;
                    try {
                        if (button.textContent.trim() === "Saved") {
                            await deleteSavedOpportunity(id);
                        } else {
                            await saveOpportunity(id);
                        }
                        await renderOpportunities();
                    } catch (error) {
                        alert(error.message || "Unable to update save state.");
                    }
                });
            });
        } catch (error) {
            resultsEl.innerHTML = `<div class="empty-state">${window.OpportunityHubAPI.escapeHtml(error.message || "Unable to load opportunities.")}</div>`;
        }
    }

    searchInput.addEventListener("input", renderOpportunities);
    categorySelect.addEventListener("change", renderOpportunities);
    modeSelect.addEventListener("change", renderOpportunities);

    await renderOpportunities();
});

