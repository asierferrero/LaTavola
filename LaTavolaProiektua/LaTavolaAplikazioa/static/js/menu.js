$(document).ready(function () {
  $.ajax({
    url: "/",
    method: "GET",
    success: function (data) {
      data.forEach(function (item, index) {
        $("#menu-items").append(`
          <div class="col-6 col-md-4">
            <div class="menu-item card">
              <img src="${item.img}" alt="${item.izena}" class="card-img-top rounded" />
              <div class="card-body">
                <h3 class="card-title">${item.izena}</h3>
                <p class="card-text">${item.deskripzioa}</p>
                <a class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#productModal-${index}">Eskatu</a>
              </div>
            </div>
          </div>
          <div class="modal fade" id="productModal-${index}" tabindex="-1" role="dialog" aria-labelledby="productModalLabel-${index}" aria-hidden="true">
            <div class="modal-dialog modal-lg" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">${item.izena}</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <div class="row">
                    <div class="col-md-5">
                      <img src="${item.img}" class="img-fluid rounded" alt="${item.izena}" />
                    </div>
                    <div class="col-md-7">
                      <p>${item.deskripzioa}</p>
                      <div class="my-3">
                        <img src="${staticUrl}img/gluten.png" style="width: 40px; height: 40px; margin-right: 10px" />
                        <img src="${staticUrl}img/huevos.png" style="width: 40px; height: 40px; margin-right: 10px" />
                        <img src="${staticUrl}img/lacteos.png" style="width: 40px; height: 40px; margin-right: 10px" />
                        <img src="${staticUrl}img/soja.png" style="width: 40px; height: 40px; margin-right: 10px" />
                      </div>
                      <h3 class="my-4">${item.prezioa}€</h3>
                      <div class="d-flex align-items-center">
                        <button class="btn btn-outline-dark btn-sm d-flex align-items-center">-</button>
                        <span class="mx-3 align-middle d-inline-flex align-items-center" style="height: 30px">1</span>
                        <button class="btn btn-outline-dark btn-sm d-flex align-items-center">+</button>
                        <img src="${staticUrl}img/cart_negro.png" style="margin-left: 20px; width: 35px; transition: opacity 0.3s ease;" onmouseout="this.src='${staticUrl}img/cart_negro.png'" onmouseover="this.src='${staticUrl}img/cart_rojo.png'" alt="Add to Cart" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `);
      });
    },
    error: function (xhr, status, error) {
      console.error("Error fetching menu items:", error);
    },
  });
});
