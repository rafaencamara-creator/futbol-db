function setupAutocomplete(inputId, tipo) {
    const input = document.getElementById(inputId);
    if (!input) return;

    let list;

    input.addEventListener("input", async function () {
        const q = this.value;
        if (q.length < 2) return;

        const res = await fetch(`/autocomplete/${tipo}?q=` + q);
        const data = await res.json();

        if (list) list.remove();

        list = document.createElement("ul");
        list.style.border = "1px solid #ccc";
        list.style.position = "absolute";
        list.style.background = "#fff";
        list.style.listStyle = "none";
        list.style.padding = "0";
        list.style.margin = "0";
        list.style.zIndex = "1000";

        data.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            li.style.padding = "4px";
            li.style.cursor = "pointer";

            li.onclick = () => {
                input.value = item;
                list.remove();
            };

            list.appendChild(li);
        });

        input.parentNode.appendChild(list);
    });

    document.addEventListener("click", () => {
        if (list) list.remove();
    });
}

