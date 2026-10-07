const token = localStorage.getItem("access_token");

if (!token) {
    window.location.href = "index.html";
}


const productList =
    document.getElementById("productList");

const addProductBtn =
    document.getElementById("addProductBtn");

const addProductForm =
    document.getElementById("addProductForm");

const cancelProductBtn =
    document.getElementById("cancelProductBtn");

const formTitle =
    document.getElementById("formTitle");

const saveProductBtn =
    document.getElementById("saveProductBtn");


let editingProductId = null;


addProductForm.style.display = "none";


addProductBtn.addEventListener(
    "click",
    function () {

        editingProductId = null;

        formTitle.textContent =
            "Add New Product";

        saveProductBtn.textContent =
            "Save Product";

        addProductForm.reset();

        addProductForm.style.display =
            "block";
    }
);


cancelProductBtn.addEventListener(
    "click",
    function () {

        addProductForm.style.display =
            "none";

        addProductForm.reset();

        editingProductId = null;
    }
);


// Load Products

async function loadProducts() {

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


        const products =
            await response.json();


        productList.innerHTML = "";


        products.forEach(
            function (product) {

                const productDiv =
                    document.createElement("div");


                productDiv.classList.add(
                    "product-item"
                );


                productDiv.innerHTML = `
                    <h3>${product.name}</h3>

                    <p>
                        Price: ${product.price}
                    </p>

                    <p>
                        Category:
                        ${product.category}
                    </p>

                    <p>
                        Description:
                        ${product.description || "No description"}
                    </p>

                    <button
                        class="edit-btn"
                        data-id="${product.id}"
                    >
                        Edit
                    </button>

                    <button
                        class="delete-btn"
                        data-id="${product.id}"
                    >
                        Delete
                    </button>
                `;


                productList.appendChild(
                    productDiv
                );
            }
        );


        // Edit buttons

        document.querySelectorAll(
            ".edit-btn"
        ).forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    async function () {

                        const productId =
                            button.dataset.id;


                        await editProduct(
                            productId
                        );
                    }
                );
            }
        );


        // Delete buttons

        document.querySelectorAll(
            ".delete-btn"
        ).forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    async function () {

                        const productId =
                            button.dataset.id;


                        await deleteProduct(
                            productId
                        );
                    }
                );
            }
        );


    } catch (error) {

        console.error(error);

        productList.innerHTML =
            "<p>Unable to load products.</p>";
    }
}


// Edit Product

async function editProduct(productId) {

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/api/products/${productId}/`,
            {
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to load product"
            );
        }


        const product =
            await response.json();


        document.getElementById(
            "productName"
        ).value = product.name;


        document.getElementById(
            "productPrice"
        ).value = product.price;


        document.getElementById(
            "productCategory"
        ).value = product.category;


        document.getElementById(
            "productDescription"
        ).value =
            product.description || "";


        editingProductId =
            productId;


        formTitle.textContent =
            "Edit Product";


        saveProductBtn.textContent =
            "Update Product";


        addProductForm.style.display =
            "block";


    } catch (error) {

        console.error(error);

        alert(
            "Unable to load product details."
        );
    }
}


// Add / Update Product

addProductForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const name =
            document.getElementById(
                "productName"
            ).value;


        const price =
            document.getElementById(
                "productPrice"
            ).value;


        const category =
            document.getElementById(
                "productCategory"
            ).value;


        const description =
            document.getElementById(
                "productDescription"
            ).value;


        const productData = {
            name: name,
            price: price,
            category: category,
            description: description
        };


        let url =
            "http://127.0.0.1:8000/api/products/";

        let method =
            "POST";


        if (editingProductId) {

            url =
                `http://127.0.0.1:8000/api/products/${editingProductId}/`;

            method =
                "PUT";
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

                    body: JSON.stringify(
                        productData
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
                    editingProductId
                        ? "Failed to update product."
                        : "Failed to add product."
                );

                return;
            }


            addProductForm.reset();

            addProductForm.style.display =
                "none";


            editingProductId = null;


            loadProducts();


        } catch (error) {

            console.error(error);

            alert(
                "Unable to connect to server."
            );
        }
    }
);


// Delete Product

async function deleteProduct(productId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this product?"
        );


    if (!confirmed) {

        return;
    }


    try {

        const response = await fetch(
            `http://127.0.0.1:8000/api/products/${productId}/`,
            {
                method: "DELETE",

                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );


        if (!response.ok) {

            const errorData =
                await response.json();

            console.error(
                errorData
            );

            alert(
                "Failed to delete product."
            );

            return;
        }


        loadProducts();


    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to server."
        );
    }
}


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

loadProducts();