document.addEventListener("DOMContentLoaded", async () => {
    if (!window.OpportunityHubAPI.requireAuth()) return;

    const id = window.OpportunityHubAPI.getQueryParam("id");
    const detailEl = document.getElementById("opportunityDetail");
    const saveBtn = document.getElementById("saveOpportunityBtn");
    const applyBtn = document.getElementById("applyOpportunityBtn");
    const messageEl = document.getElementById("detailMessage");
    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            window.OpportunityHubAPI.clearToken();
            window.location.href = "login.html";
        });
    }

    if (!id) {
        detailEl.innerHTML = '<div class="empty-state">No opportunity selected.</div>';
        return;
    }

    let saved = false;

    function showMessage(text, kind = "info") {
        messageEl.textContent = text;
        messageEl.className = `detail-message detail-message--${kind}`;
    }

    async function syncSavedState() {
        try {
            const savedList = await window.OpportunityHubAPI.listSavedOpportunities();
            saved = savedList.some((item) => Number(item.id) === Number(id));
            saveBtn.textContent = saved ? "Unsave" : "Save";
            saveBtn.classList.toggle("btn-primary", !saved);
            saveBtn.classList.toggle("btn-secondary", saved);
        } catch (error) {
            saved = false;
        }
    }

    try {
        const opportunity = await window.OpportunityHubAPI.getOpportunity(id);
        const skills = (opportunity.skills || []).map((item) => `<span class="tag">${window.OpportunityHubAPI.escapeHtml(item)}</span>`).join("");
        const eligibility = opportunity.eligibility || "Open to eligible students.";
        detailEl.innerHTML = `
            <div class="opportunity-detail__header">
                <div>
                    <p class="eyebrow-alt">${window.OpportunityHubAPI.escapeHtml(opportunity.category || "Opportunity")}</p>
                    <h1>${window.OpportunityHubAPI.escapeHtml(opportunity.title || "Untitled")}</h1>
                    <p class="detail-org">${window.OpportunityHubAPI.escapeHtml(opportunity.organization || "Unknown org")}</p>
                </div>
                <span class="match-badge large">${window.OpportunityHubAPI.escapeHtml(opportunity.mode || "Any")}</span>
            </div>
            <p class="detail-description">${window.OpportunityHubAPI.escapeHtml(opportunity.description || "No description available.")}</p>
            <div class="detail-meta-grid">
                <div class="meta-box"><span>Location</span><strong>${window.OpportunityHubAPI.escapeHtml(opportunity.location || "Remote")}</strong></div>
                <div class="meta-box"><span>Deadline</span><strong>${window.OpportunityHubAPI.formatDate(opportunity.deadline)}</strong></div>
                <div class="meta-box"><span>Mode</span><strong>${window.OpportunityHubAPI.escapeHtml(window.OpportunityHubAPI.formatMode(opportunity.mode))}</strong></div>
                <div class="meta-box"><span>Apply</span><strong>${window.OpportunityHubAPI.escapeHtml(opportunity.application_url || "Website")}</strong></div>
            </div>
            <div class="tags-wrap">${skills}</div>
            <div class="detail-section">
                <h3>Eligibility</h3>
                <p>${window.OpportunityHubAPI.escapeHtml(eligibility)}</p>
            </div>
            <div class="detail-section">
                <h3>Benefits</h3>
                <p>${window.OpportunityHubAPI.escapeHtml(opportunity.benefits || "Check the application page for more details.")}</p>
            </div>
        `;

        await syncSavedState();
    } catch (error) {
        detailEl.innerHTML = `<div class="empty-state">${window.OpportunityHubAPI.escapeHtml(error.message || "Opportunity not found.")}</div>`;
        saveBtn.disabled = true;
        applyBtn.disabled = true;
        return;
    }

    saveBtn.addEventListener("click", async () => {
        try {
            if (saved) {
                await window.OpportunityHubAPI.deleteSavedOpportunity(id);
                saved = false;
                saveBtn.textContent = "Save";
                showMessage("Removed from saved opportunities.", "success");
            } else {
                await window.OpportunityHubAPI.saveOpportunity(id);
                saved = true;
                saveBtn.textContent = "Unsave";
                showMessage("Opportunity saved to your list.", "success");
            }
            saveBtn.classList.toggle("btn-primary", !saved);
            saveBtn.classList.toggle("btn-secondary", saved);
        } catch (error) {
            showMessage(error.message || "Unable to update save state.", "error");
        }
    });

    applyBtn.addEventListener("click", async () => {
        try {
            await window.OpportunityHubAPI.createApplication(id, "Interested", "Applied from the demo flow.");
            showMessage("Application submitted successfully.", "success");
        } catch (error) {
            showMessage(error.message || "Unable to apply.", "error");
        }
    });
});

