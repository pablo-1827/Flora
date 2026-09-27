const API_BASE_URL = "https://opportunityhub-api-h8xi.onrender.com/api/v1";

function getToken() {
    return localStorage.getItem("opportunityhub_token");
}

function setToken(token) {
    localStorage.setItem("opportunityhub_token", token);
}

function clearToken() {
    localStorage.removeItem("opportunityhub_token");
}

function requireAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = "login.html";
        return false;
    }
    return true;
}

async function apiRequest(path, options = {}) {
    const headers = {
        ...(options.headers || {}),
    };

    const token = getToken();
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    if (options.body && !(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    const response = await fetch(`${API_BASE_URL}${path}`, {
        ...options,
        headers,
    });

    const contentType = response.headers.get("content-type") || "";
    let payload = null;
    if (contentType.includes("application/json")) {
        payload = await response.json();
    } else if (response.status !== 204) {
        const text = await response.text();
        payload = text ? { detail: text } : null;
    }

    if (!response.ok) {
        const detail = payload?.detail || "Request failed.";
        throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }

    return payload;
}

async function registerUser(payload) {
    return apiRequest("/auth/register", {
        method: "POST",
        body: JSON.stringify(payload),
    });
}

async function loginUser(payload) {
    const result = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify(payload),
    });
    if (result?.access_token) {
        setToken(result.access_token);
    }
    return result;
}

async function getCurrentUser() {
    return apiRequest("/auth/me");
}

async function getProfile() {
    return apiRequest("/profile");
}

async function createProfile(payload) {
    return apiRequest("/profile", {
        method: "POST",
        body: JSON.stringify(payload),
    });
}

async function listOpportunities(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== "") {
            query.append(key, value);
        }
    });
    const url = query.toString() ? `?${query.toString()}` : "";
    return apiRequest(`/opportunities${url}`);
}

async function getOpportunity(id) {
    return apiRequest(`/opportunities/${id}`);
}

async function getRecommendations() {
    return apiRequest("/recommendations");
}

async function listSavedOpportunities() {
    return apiRequest("/saved-opportunities");
}

async function saveOpportunity(opportunityId) {
    return apiRequest("/saved-opportunities", {
        method: "POST",
        body: JSON.stringify({ opportunity_id: Number(opportunityId) }),
    });
}

async function deleteSavedOpportunity(opportunityId) {
    return apiRequest(`/saved-opportunities/${opportunityId}`, {
        method: "DELETE",
    });
}

async function listApplications() {
    return apiRequest("/applications");
}

async function createApplication(opportunityId, status = "Interested", note = "") {
    return apiRequest("/applications", {
        method: "POST",
        body: JSON.stringify({
            opportunity_id: Number(opportunityId),
            status,
            note,
        }),
    });
}

function getQueryParam(name) {
    return new URLSearchParams(window.location.search).get(name);
}

function formatDate(value) {
    if (!value) return "No deadline";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}

function formatMode(mode) {
    if (!mode) return "Any";
    return mode.charAt(0).toUpperCase() + mode.slice(1);
}

function escapeHtml(value) {
    return String(value || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

window.OpportunityHubAPI = {
    getToken,
    setToken,
    clearToken,
    requireAuth,
    apiRequest,
    registerUser,
    loginUser,
    getCurrentUser,
    getProfile,
    createProfile,
    listOpportunities,
    getOpportunity,
    getRecommendations,
    listSavedOpportunities,
    saveOpportunity,
    deleteSavedOpportunity,
    listApplications,
    createApplication,
    getQueryParam,
    formatDate,
    formatMode,
    escapeHtml,
};

