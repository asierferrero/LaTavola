document.addEventListener("DOMContentLoaded", function () {
    fetch("/static/json/pizzak.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error al cargar el archivo JSON");
        }
        return response.json();
      })
      .then((data) => {
        const menuItemsContainer = document.getElementById("menu-items");
  
        data.forEach((item) => {
            const modalId = `modal-${item.id}`;
            const menuItem = document.createElement("div");
            menuItem.className = "col-6 col-md-4";
            menuItem.innerHTML = `
              <div class="menu-item card">
                <img src="${item.imagen_url}" alt="${item.nombre}" class="card-img-top rounded" />
                <div class="card-body">
                  <h3 class="card-title">${item.nombre}</h3>
                  <p class="card-text">${item.descripcion}</p>
                  <button class="btn btn-danger" data-toggle="modal" data-target="#${modalId}">Eskatu</button>
                </div>
              </div>   
          
              <div class="modal fade" id="${modalId}" tabindex="-1" role="dialog" aria-labelledby="${modalId}Label" aria-hidden="true">
                <div class="modal-dialog modal-lg" role="document">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="${modalId}Label">${item.nombre}</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    <div class="modal-body">
                      <div class="row">
                        <div class="col-md-5">
                          <img src="${item.imagen_url}" class="img-fluid rounded"/>
                        </div>
                        <div class="col-md-7">
                          <p>${item.descripcion}</p>
                          <div class="my-3">
                            <img src="${item.imagen_url}" style="width: 40px; height: 40px; margin-right: 10px" />
                            <img src="${item.imagen_url}" style="width: 40px; height: 40px; margin-right: 10px" />
                            <img src="${item.imagen_url}" style="width: 40px; height: 40px; margin-right: 10px" />
                            <img src="${item.imagen_url}" style="width: 40px; height: 40px; margin-right: 10px" />
                          </div>
                          <h3 class="my-4">15.99€</h3>
                          <div class="d-flex align-items-center">
                            <button class="btn btn-outline-dark">-</button>
                            <span class="mx-3">1</span>
                            <button class="btn btn-outline-dark">+</button>
                            <button class="btn btn-danger ml-3">
                              <img src="${item.imagen_url}" width="20px" alt="Add to Cart" />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            `;
            menuItemsContainer.appendChild(menuItem);
          });
      })
      .catch((error) => console.error("Error al cargar el menú:", error));
  });
  