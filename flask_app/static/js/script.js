console.log("connected")

function toggleRows(parentId, btn) {

    const open = btn.innerText === "▼";
    btn.innerText = open ? "▶" : "▼";

    document.querySelectorAll(`[data-parent='${parentId}']`)
        .forEach(row => row.classList.toggle("d-none", open));
}

function filterBOM() {
    const input = document.getElementById("bomSearch").value.toLowerCase();
    const rows = document.querySelectorAll("tbody tr");

    let showParents = new Set();

    // First pass: find matching rows
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        const isMatch = text.includes(input);

        row.style.display = isMatch ? "" : "none";

        // if device matches, show its parent tag row
        if (isMatch && row.dataset.parent) {
            showParents.add(row.dataset.parent);
        }

        // if tag row matches, mark it
        if (isMatch && row.dataset.id) {
            showParents.add(row.dataset.id);
        }
    });

    // Second pass: make sure parent rows are visible
    rows.forEach(row => {
        if (row.dataset.id && showParents.has(row.dataset.id)) {
            row.style.display = "";
        }
        if (row.dataset.parent && showParents.has(row.dataset.parent)) {
            row.style.display = "";
        }
    });
}