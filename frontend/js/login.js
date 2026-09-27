document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const rememberInput = document.getElementById("remember");
    const passwordToggle = document.getElementById("passwordToggle");
    const passwordToggleText = document.getElementById("passwordToggleText");
    const loginButton = document.getElementById("loginButton");
    const loginButtonText = document.getElementById("loginButtonText");
    const authMessage = document.getElementById("authMessage");

    if (new URLSearchParams(window.location.search).get("registered") === "1") {
        authMessage.textContent = "Account created successfully. Please log in.";
        authMessage.classList.add("is-visible");
        authMessage.style.borderColor = "rgba(106, 190, 120, 0.35)";
        authMessage.style.background = "rgba(21, 187, 120, 0.08)";
        authMessage.style.color = "#baf3d2";
    }

    if (passwordToggle && passwordToggleText) {
        passwordToggle.addEventListener("click", () => {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";
            passwordToggleText.textContent = isPassword ? "Hide" : "Show";
            passwordToggle.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
        });
    }

    function showMessage(message, isError = false) {
        authMessage.textContent = message;
        authMessage.classList.add("is-visible");
        authMessage.style.borderColor = isError ? "rgba(213, 26, 43, 0.25)" : "rgba(106, 190, 120, 0.35)";
        authMessage.style.background = isError ? "rgba(213, 26, 43, 0.08)" : "rgba(21, 187, 120, 0.08)";
        authMessage.style.color = isError ? "#ffb0b7" : "#baf3d2";
    }

    function hideMessage() {
        authMessage.textContent = "";
        authMessage.classList.remove("is-visible");
    }

    if (!rememberInput) {
        window.OpportunityHubAPI.clearToken();
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        hideMessage();

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        loginButton.disabled = true;
        loginButtonText.textContent = "Logging in…";

        try {
            const result = await window.OpportunityHubAPI.loginUser({
                email: emailInput.value.trim(),
                password: passwordInput.value,
            });

            if (!result || !result.access_token) {
                throw new Error("Login failed: missing access token.");
            }

            window.location.href = "dashboard.html";
        } catch (error) {
            showMessage(error.message || "Unable to log in right now.", true);
            loginButton.disabled = false;
            loginButtonText.textContent = "Log in";
        }
    });
});

