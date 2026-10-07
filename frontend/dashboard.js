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