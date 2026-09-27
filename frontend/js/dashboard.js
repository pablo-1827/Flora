document.addEventListener("DOMContentLoaded", async () => {
    if (!window.OpportunityHubAPI.requireAuth()) return;

    const { getCurrentUser, getProfile, getRecommendations, listSavedOpportunities, listApplications } = window.OpportunityHubAPI;
    const profileNameEl = document.getElementById("welcomeName");
    const profileMetaEl = document.getElementById("profileMeta");
    const recommendationListEl = document.getElementById("recommendationsList");
    const statOpportunityEl = document.getElementById("statOpportunityCount");
    const statSavedEl = document.getElementById("statSavedCount");
    const statApplicationsEl = document.getElementById("statApplicationsCount");
    const statBestEl = document.getElementById("statBestMatch");
    const emptyStateEl = document.getElementById("recommendationsEmpty");

    const logoutButton = document.getElementById("logoutButton");
    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            window.OpportunityHubAPI.clearToken();
            window.location.href = "login.html";
        });
    }

    try {
        const [user, profile, recommendations, saved, applications] = await Promise.all([
            getCurrentUser(),
            getProfile(),
            getRecommendations(),
            listSavedOpportunities(),
            listApplications(),
        ]);

        const firstName = user.full_name?.split(" ")[0] || "Student";
        profileNameEl.textContent = `Welcome back, ${firstName}!`;
        profileMetaEl.textContent = `${profile.college || "Your college"} • ${profile.degree || "Your degree"}`;

        const bestMatch = recommendations.length ? Math.max(...recommendations.map((item) => Number(item.relevance_score || 0))) : 0;
        statOpportunityEl.textContent = recommendations.length;
        statSavedEl.textContent = saved.length;
        statApplicationsEl.textContent = applications.length;
        statBestEl.textContent = `${bestMatch}%`;

        if (!recommendations.length) {
            emptyStateEl.hidden = false;
            recommendationListEl.innerHTML = "";
            return;
        }

        emptyStateEl.hidden = true;
        recommendationListEl.innerHTML = recommendations.slice(0, 4).map((item) => {
            const opportunity = item.opportunity || {};
            const score = Number(item.relevance_score || 0);
            return `
                <article class="opportunity-card dashboard-card">
                    <div class="opportunity-card__top">
                        <div>
                            <h3 class="opportunity-card__title">${window.OpportunityHubAPI.escapeHtml(opportunity.title || "Untitled")}</h3>
                            <p class="opportunity-card__org">${window.OpportunityHubAPI.escapeHtml(opportunity.organization || "Unknown org")}</p>
                        </div>
                        <span class="match-badge">${score}%</span>
                    </div>
                    <div class="opportunity-card__meta">
                        <span>${window.OpportunityHubAPI.escapeHtml(opportunity.mode || "Any")}</span>
                        <span>•</span>
                        <span>${window.OpportunityHubAPI.escapeHtml(opportunity.location || "Remote")}</span>
                        <span>•</span>
                        <span>${window.OpportunityHubAPI.escapeHtml(opportunity.category || "Opportunity")}</span>
                    </div>
                    <p class="recommendation-description">${window.OpportunityHubAPI.escapeHtml(item.explanation || "Good match for your profile.")}</p>
                    <div class="card-actions">
                        <a class="btn btn-secondary small" href="opportunity.html?id=${opportunity.id}">View</a>
                    </div>
                </article>
            `;
        }).join("");
    } catch (error) {
        const message = error?.message || "Unable to load dashboard.";
        recommendationListEl.innerHTML = `<div class="empty-state">${window.OpportunityHubAPI.escapeHtml(message)}</div>`;
        emptyStateEl.hidden = true;
    }
});

