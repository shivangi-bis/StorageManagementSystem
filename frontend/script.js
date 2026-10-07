const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/token/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem(
                "access_token",
                data.access
            );

            localStorage.setItem(
                "refresh_token",
                data.refresh
            );

            message.textContent = "Login successful!";

            window.location.href = "dashboard.html";

            console.log("Login successful");
            console.log(data);

        } else {

            message.textContent =
                "Invalid username or password.";

        }

    } catch (error) {

        message.textContent =
            "Unable to connect to server.";

        console.error(error);
    }
});