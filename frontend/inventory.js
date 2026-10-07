const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "index.html";
}


const inventoryList =
    document.getElementById("inventoryList");

const addInventoryBtn =
    document.getElementById("addInventoryBtn");

const addInventoryForm =
    document.getElementById("addInventoryForm");

const cancelInventoryBtn =
    document.getElementById("cancelInventoryBtn");

const inventoryProductSelect =
    document.getElementById("inventoryProduct");

const inventoryFormTitle =
    document.getElementById("inventoryFormTitle");

const saveInventoryBtn =
    document.getElementById("saveInventoryBtn");


let allProducts = [];

let editingInventoryId = null;


// Initially hide form

addInventoryForm.style.display = "none";


// Show Add Inventory Form

addInventoryBtn.addEventListener(
    "click",
    function () {

        editingInventoryId = null;

        inventoryFormTitle.textContent =
            "Add Inventory Entry";

        saveInventoryBtn.textContent =
            "Save";

        addInventoryForm.reset();

        inventoryProductSelect.disabled = false;

        addInventoryForm.style.display =
            "block";
    }
);


// Hide Form

cancelInventoryBtn.addEventListener(
    "click",
    function () {

        addInventoryForm.style.display =
            "none";

        addInventoryForm.reset();

        editingInventoryId = null;

        inventoryProductSelect.disabled = false;
    }
);


// Load Products

async function loadProductsForDropdown() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/products/",
            {
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to load products"
            );
        }


        allProducts =
            await response.json();


        inventoryProductSelect.innerHTML =
            '<option value="">-- Select Product --</option>';


        allProducts.forEach(
            function (product) {

                const option =
                    document.createElement("option");


                option.value =
                    product.id;


                option.textContent =
                    product.name;


                inventoryProductSelect.appendChild(
                    option
                );
            }
        );


    } catch (error) {

        console.error(error);
    }
}


// Load Inventory

async function loadInventory() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/inventory/",
            {
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to load inventory"
            );
        }


        const inventoryItems =
            await response.json();


        inventoryList.innerHTML = "";


        inventoryItems.forEach(
            function (item) {

                const matchedProduct =
                    allProducts.find(
                        function (product) {

                            return product.id ===
                                item.product;
                        }
                    );


                const productName =
                    matchedProduct
                        ? matchedProduct.name
                        : "Unknown Product";


                const itemDiv =
                    document.createElement("div");


                itemDiv.classList.add(
                    "inventory-item"
                );


                itemDiv.innerHTML = `
                    <h3>${productName}</h3>

                    <p>
                        Quantity:
                        ${item.quantity}

                        ${
                             item.low_stock
                                ? '<span class="low-stock">⚠️ Low Stock</span>'
                                : ''
                        }
                    </p>

                    <p>
                        Last updated:
                        ${new Date(
                            item.updated_at
                        ).toLocaleString()}
                    </p>

                    <button
                        class="edit-inventory-btn"
                        data-id="${item.id}"
                    >
                        Update
                    </button>
                `;


                inventoryList.appendChild(
                    itemDiv
                );
            }
        );


        // Update buttons

        document.querySelectorAll(
            ".edit-inventory-btn"
        ).forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    async function () {

                        const inventoryId =
                            button.dataset.id;


                        await editInventory(
                            inventoryId
                        );
                    }
                );
            }
        );


    } catch (error) {

        console.error(error);

        inventoryList.innerHTML =
            "<p>Unable to load inventory.</p>";
    }
}


// Edit Inventory

async function editInventory(inventoryId) {

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/api/inventory/${inventoryId}/`,
            {
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to load inventory"
            );
        }


        const inventory =
            await response.json();


        editingInventoryId =
            inventoryId;


        inventoryProductSelect.value =
            inventory.product;


        document.getElementById(
            "inventoryQuantity"
        ).value =
            inventory.quantity;


        inventoryProductSelect.disabled =
            true;


        inventoryFormTitle.textContent =
            "Update Inventory";


        saveInventoryBtn.textContent =
            "Update";


        addInventoryForm.style.display =
            "block";


    } catch (error) {

        console.error(error);

        alert(
            "Unable to load inventory details."
        );
    }
}


// Add / Update Inventory

addInventoryForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const productId =
            inventoryProductSelect.value;


        const quantity =
            document.getElementById(
                "inventoryQuantity"
            ).value;


        let url =
            "http://127.0.0.1:8000/api/inventory/";

        let method =
            "POST";


        let requestData = {
            product: productId,
            quantity: quantity
        };


        if (editingInventoryId) {

            url =
                `http://127.0.0.1:8000/api/inventory/${editingInventoryId}/`;

            method =
                "PATCH";

            requestData = {
                quantity: quantity
            };
        }


        try {

            const response = await fetch(
                url,
                {
                    method: method,

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`
                    },

                    body:
                        JSON.stringify(
                            requestData
                        )
                }
            );


            if (!response.ok) {

                const errorData =
                    await response.json();

                console.error(
                    errorData
                );

                alert(
                    editingInventoryId
                        ? "Failed to update inventory."
                        : "Failed to add inventory."
                );

                return;
            }


            addInventoryForm.reset();

            addInventoryForm.style.display =
                "none";


            inventoryProductSelect.disabled =
                false;


            editingInventoryId =
                null;


            loadInventory();


        } catch (error) {

            console.error(error);

            alert(
                "Unable to connect to server."
            );
        }
    }
);


// Logout

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


// Initial loading

async function init() {

    await loadProductsForDropdown();

    await loadInventory();
}


init();