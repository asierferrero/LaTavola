document.addEventListener("DOMContentLoaded", function() {
    fetch("/static/json/pizzak.json")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al cargar el archivo JSON");
            }
            return response.json();
        })
        .then(data => {
            const menuItemsContainer = document.getElementById("menu-items");

            data.forEach(item => {
                const menuItem = document.createElement("div");
                menuItem.className = "col-md-4";
                menuItem.innerHTML = `
                    <div class="menu-item card">
                        <img src="${item.imagen_url}" alt="${item.nombre}" class="card-img-top rounded" />
                        <div class="card-body">
                            <h3 class="card-title">${item.nombre}</h3>
                            <p class="card-text">${item.descripcion}</p>
                            <a class="btn btn-danger">Eskatu</a>
                        </div>
                    </div>
                `;
                menuItemsContainer.appendChild(menuItem);
            });
        })
        .catch(error => console.error("Error al cargar el menú:", error));
});
