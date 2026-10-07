const token = localStorage.getItem("access_token");

const tableBody = document.getElementById("historyTableBody");

if (!token) {
    window.location.href = "login.html";
}

fetch("http://127.0.0.1:8000/api/stock-history/", {
    headers: {
        "Authorization": `Bearer ${token}`
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error("Failed to fetch stock history");
    }

    return response.json();
})
.then(data => {

    tableBody.innerHTML = "";

    if (data.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="5">No stock history found.</td>
            </tr>
        `;
        return;
    }

    data.forEach(item => {

        const row = document.createElement("tr");

        const movementClass =
            item.movement_type === "IN"
                ? "stock-in"
                : "stock-out";

        const sign =
            item.movement_type === "IN"
                ? "+"
                : "-";

        const date = new Date(item.created_at).toLocaleString();

        row.innerHTML = `
            <td>${item.product_name}</td>

            <td>
                <span class="${movementClass}">
                    ${item.movement_type}
                </span>
            </td>

            <td>
                ${sign}${item.quantity}
            </td>

            <td>
                ${item.reason}
            </td>

            <td>
                ${date}
            </td>
        `;

        tableBody.appendChild(row);
    });

})
.catch(error => {
    console.error(error);

    tableBody.innerHTML = `
        <tr>
            <td colspan="5">
                Failed to load stock history.
            </td>
        </tr>
    `;
});