const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "index.html";
}


const orderList = document.getElementById("orderList");

const addOrderBtn = document.getElementById("addOrderBtn");
const addOrderForm = document.getElementById("addOrderForm");
const cancelOrderBtn = document.getElementById("cancelOrderBtn");
const orderProductSelect = document.getElementById("orderProduct");


// Initially hide form
addOrderForm.style.display = "none";


// Show form
addOrderBtn.addEventListener("click", function () {
    addOrderForm.style.display = "block";
});


// Hide form
cancelOrderBtn.addEventListener("click", function () {
    addOrderForm.style.display = "none";
    addOrderForm.reset();
});


// Store products globally for dropdown + name lookup
let allProducts = [];


// Load Products (for dropdown + name lookup)
async function loadProductsForDropdown() {

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/products/",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to load products");
        }

        allProducts = await response.json();

        orderProductSelect.innerHTML =
            '<option value="">-- Select Product --</option>';

        allProducts.forEach(function (product) {

            const option = document.createElement("option");

            option.value = product.id;
            option.textContent = product.name;

            orderProductSelect.appendChild(option);
        });

    } catch (error) {
        console.error(error);
    }
}


// Load Orders
async function loadOrders() {

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/orders/",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to load orders");
        }

        const orders = await response.json();

        orderList.innerHTML = "";

        orders.forEach(function (order) {

            // order.product is just an ID — find matching product name
            const matchedProduct = allProducts.find(
                function (p) {
                    return p.id === order.product;
                }
            );

            const productName = matchedProduct
                ? matchedProduct.name
                : "Unknown Product";

            const orderDiv = document.createElement("div");
            orderDiv.classList.add("order-item");

            orderDiv.innerHTML = `
                <h3>${productName}</h3>
                <p>Quantity: ${order.quantity}</p>
                <p>Ordered on: ${new Date(order.created_at).toLocaleString()}</p>
            `;

            orderList.appendChild(orderDiv);
        });

    } catch (error) {
        console.error(error);
        orderList.innerHTML = "<p>Unable to load orders.</p>";
    }
}


// Create Order
addOrderForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const productId = orderProductSelect.value;
    const quantity = document.getElementById("orderQuantity").value;

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/orders/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    product: productId,
                    quantity: quantity
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            // Backend sends {"detail": "Insufficient stock."} on failure
            const errorMessage =
                data.detail || "Failed to place order.";

            alert(errorMessage);

            console.error(data);
            return;
        }

        addOrderForm.reset();
        addOrderForm.style.display = "none";

        loadOrders();

    } catch (error) {
        console.error(error);
        alert("Unable to connect to server.");
    }
});


// Logout
document.getElementById("logoutBtn").addEventListener("click", function () {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "index.html";
});


// Initial loading — products first, then orders (so name lookup works)
async function init() {
    await loadProductsForDropdown();
    await loadOrders();
}

init();