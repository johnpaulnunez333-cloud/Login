function loginPage() {
    const form = document.getElementById('loginInput');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const usernameValue = document.getElementById('username').value;
        const emailValue = document.getElementById('email').value;
        const passwordValue = document.getElementById('password').value;

        if (usernameValue === "" || emailValue === "" || passwordValue === "") {
            alert("Please fill out all fields.");
            return;
        }

        try {
            const response = await fetch("https://your-backend.com/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: usernameValue,
                    email: emailValue,
                    password: passwordValue
                })
            });

            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }

            const data = await response.json();
            console.log("Server response:", data);

            if (data.success) {
                alert("Login Successful");
                // e.g. redirect, store token, etc.
                // localStorage.setItem("token", data.token);
            } else {
                alert(data.message || "Login failed.");
            }

        } catch (error) {
            console.error("Login request failed:", error);
            alert("Something went wrong. Please try again.");
        }
    });
}

loginPage();