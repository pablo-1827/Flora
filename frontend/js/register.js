document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");

    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const collegeInput = document.getElementById("college");
    const degreeInput = document.getElementById("degree");
    const branchInput = document.getElementById("branch");
    const yearInput = document.getElementById("year");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");

    const passwordToggle = document.getElementById("passwordToggle");
    const passwordToggleText = document.getElementById("passwordToggleText");

    const registerButton = document.getElementById("registerButton");
    const registerButtonText = document.getElementById("registerButtonText");

    const authMessage = document.getElementById("authMessage");

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
        authMessage.style.borderColor = "rgba(213, 26, 43, 0.25)";
        authMessage.style.background = "rgba(213, 26, 43, 0.08)";
        authMessage.style.color = "#ffb0b7";
    }

    passwordToggle.addEventListener("click", () => {
        const isPassword = password.type === "password";
        password.type = isPassword ? "text" : "password";
        passwordToggleText.textContent = isPassword ? "Hide" : "Show";
        passwordToggle.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
    });

    confirmPassword.addEventListener("input", () => {
        if (confirmPassword.value && password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity("Passwords do not match.");
        } else {
            confirmPassword.setCustomValidity("");
        }
    });

    password.addEventListener("input", () => {
        if (confirmPassword.value && password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity("Passwords do not match.");
        } else {
            confirmPassword.setCustomValidity("");
        }
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        hideMessage();

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        if (password.value !== confirmPassword.value) {
            showMessage("Passwords do not match.", true);
            confirmPassword.focus();
            return;
        }

        registerButton.disabled = true;
        registerButtonText.textContent = "Creating account…";

        try {
            const userPayload = {
                name: nameInput.value.trim(),
                email: emailInput.value.trim(),
                password: password.value,
            };

            await window.OpportunityHubAPI.registerUser(userPayload);

            const loginResult = await window.OpportunityHubAPI.loginUser({
                email: emailInput.value.trim(),
                password: password.value,
            });

            if (!loginResult || !loginResult.access_token) {
                throw new Error("Account created, but login failed.");
            }

            const yearMap = {
                "1": "1st Year",
                "2": "2nd Year",
                "3": "3rd Year",
                "4": "4th Year",
                "5": "Postgraduate",
            };

            const registrationYear = Number(yearInput.value || 1);
            const currentYear = new Date().getFullYear();
            const graduationYear = registrationYear >= 5 ? currentYear + 1 : currentYear + (5 - registrationYear);

            const profilePayload = {
                full_name: nameInput.value.trim(),
                college: collegeInput.value.trim(),
                degree: degreeInput.value.trim(),
                branch: branchInput.value.trim(),
                current_academic_year: yearMap[yearInput.value] || "1st Year",
                graduation_year: graduationYear,
                skills: [],
                interests: [],
                categories: [],
                preferred_mode: "any",
                preferred_location: "",
                resume_url: "",
            };

            await window.OpportunityHubAPI.createProfile(profilePayload);
            window.OpportunityHubAPI.clearToken();
            window.location.href = "login.html?registered=1";
        } catch (error) {
            showMessage(error.message || "Unable to create your account right now.", true);
            registerButton.disabled = false;
            registerButtonText.textContent = "Create my account";
        }
    });
});

