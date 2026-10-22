const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "index.html";
}

const productCount = document.getElementById("productCount");
const inventoryCount = document.getElementById("inventoryCount");
const orderCount = document.getElementById("orderCount");
const lowStockCount = document.getElementById("lowStockCount");
const recentMovements = document.getElementById("recentMovements");


async function loadDashboard() {

    try {

        const headers = {
            "Authorization": `Bearer ${token}`
        };


        const [
            productsResponse,
            inventoryResponse,
            ordersResponse,
            historyResponse
        ] = await Promise.all([

            fetch(
                "http://127.0.0.1:8000/api/products/",
                { headers: headers }
            ),

            fetch(
                "http://127.0.0.1:8000/api/inventory/",
                { headers: headers }
            ),

            fetch(
                "http://127.0.0.1:8000/api/orders/",
                { headers: headers }
            ),

            fetch(
                "http://127.0.0.1:8000/api/stock-history/",
                { headers: headers }
            )

        ]);


        const products =
            await productsResponse.json();

        const inventory =
            await inventoryResponse.json();

        const orders =
            await ordersResponse.json();

        const history =
            await historyResponse.json();


        productCount.textContent =
            products.length;

        inventoryCount.textContent =
            inventory.length;

        orderCount.textContent =
            orders.length;

        const lowStockItems =
            inventory.filter(function (item){
                return item.low_stock == true;
            });


        lowStockCount.textContent=
            lowStockItems.length;

        recentMovements.innerHTML = "";

        const recentHistory = history.slice(0, 5);

        if (recentHistory.length === 0) {
            recentMovements.innerHTML =
                "<p>No stock movements found.</p>";
        } else {
            recentHistory.forEach(function (item) {

            const movement = document.createElement("p");

            const sign =
                item.movement_type === "IN"
                    ? "+"
                    : "-";

            movement.innerHTML = `
                <strong>${item.product_name}</strong>
                — ${item.movement_type}
                ${sign}${item.quantity}
                — ${item.reason}
             `;

            recentMovements.appendChild(movement);
        });
    } 


    } catch (error) {

        console.error(
            "Dashboard loading error:",
            error
        );
    }
}


document.getElementById(
    "logoutBtn"
).addEventListener(
    "click",
    function () {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "refresh_token"
        );

        window.location.href =
            "index.html";
    }
);


loadDashboard();
console.log("Dashboard JavaScript loaded");


const chatToggle = document.getElementById("chatToggle");
const chatWidget = document.getElementById("chatWidget");
const chatClose = document.getElementById("chatClose");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
const chatSend = document.getElementById("chatSend");

chatToggle.addEventListener("click", function () {
    chatWidget.classList.remove("hidden");
    chatInput.focus();
});

chatClose.addEventListener("click", function () {
    chatWidget.classList.add("hidden");
});

function addChatMessage(message, sender) {
    const bubble = document.createElement("div");
    bubble.className = sender === "user" ? "user-message" : "bot-message";
    bubble.textContent = message;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const question = chatInput.value.trim();
    if (!question) return;

    addChatMessage(question, "user");
    chatInput.value = "";
    chatSend.disabled = true;

    const loading = document.createElement("div");
    loading.className = "bot-message";
    loading.textContent = "Thinking...";
    chatMessages.appendChild(loading);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch("http://127.0.0.1:8000/api/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify({ question: question })
        });

        const result = await response.json();
        loading.remove();

        if (response.status === 401 || response.status === 403) {
            addChatMessage("Your session may have expired. Please log in again.", "bot");
        } else if (!response.ok) {
            addChatMessage(result.error || "Sorry, something went wrong.", "bot");
        } else {
            let answer = result.answer;

            // Convert JSON-formatted answers into readable text.
            try {
                const parsed = JSON.parse(answer);
                if (parsed && typeof parsed === "object") {
                    answer = JSON.stringify(parsed, null, 2);
                } else {
                    answer = String(parsed);
                }
            } catch {
                // Keep the original answer if it is not JSON.
            }

            addChatMessage(answer || "I couldn't find an answer.", "bot");
        }
    } catch (error) {
        loading.remove();
        addChatMessage("Could not connect to the server. Please check that Django and Ollama are running.", "bot");
        console.error("Chatbot error:", error);
    } finally {
        chatSend.disabled = false;
        chatInput.focus();
    }
});
