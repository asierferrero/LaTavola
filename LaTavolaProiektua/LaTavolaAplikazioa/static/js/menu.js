$(document).ready(function () {
  $.ajax({
    url: "/api/produktuak/",
    method: "GET",
    success: function (data) {
      data.forEach(function (item, index) {
        let alergenoak = item.alergenoak.map(alergeno => `
          <img src="${alergeno.img}" style="width: 40px; height: 40px; margin-right: 10px" title="${alergeno.izena}" />
        `).join('');

        $("#menu-items").append(`
          <div class="col-12 col-md-2">
            <div class="menu-item card">
              <img src="${item.img}" alt="${item.izena}" class="card-img-top rounded" />
              <div class="card-body text-start">
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
                  <h2 class="modal-title">${item.izena}</h2>
                  <button type="button" class="btn-danger" data-bs-dismiss="modal">X</button>
                </div>
                <div class="modal-body text-start">
                  <div class="row">
                    <div class="col-md-4">
                      <img src="${item.img}" class="img-fluid rounded" alt="${item.izena}" />
                    </div>
                    <div class="col-md-7">
                      <p>${item.deskripzioa}</p>
                      <div class="my-3">
                        ${alergenoak}
                      </div>
                      <h3 class="my-4">${item.prezioa}€</h3>
                      <div class="d-flex">
                        <button class="btn btn-outline-dark btn-sm d-flex decrement" data-index="${index}">-</button>
                        <span class="mx-3 align-middle d-inline-flex quantity" data-index="${index}" style="height: 30px">1</span>
                        <button class="btn btn-outline-dark btn-sm d-flex increment" data-index="${index}" data-stock="${item.stock}">+</button>
                        <img src="${staticUrl}img/cart_negro.png" style="margin-left: 20px; width: 35px; transition: opacity 0.3s ease;" onmouseout="this.src='${staticUrl}img/cart_negro.png'" onmouseover="this.src='${staticUrl}img/cart_rojo.png'" alt="Add to Cart" class="add-to-cart" data-name="${item.izena}" data-price="${item.prezioa}" data-index="${index}" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `);
      });

      $(".increment").click(function () {
        const index = $(this).data("index");
        const stock = parseInt($(this).data("stock"));
        let quantityElement = $(`.quantity[data-index="${index}"]`);
        let quantity = parseInt(quantityElement.text());

        if (quantity < stock) {
          quantityElement.text(quantity + 1);
        }
      });

      $(".decrement").click(function () {
        const index = $(this).data("index");
        let quantityElement = $(`.quantity[data-index="${index}"]`);
        let quantity = parseInt(quantityElement.text());
        if (quantity > 1) {
          quantityElement.text(quantity - 1);
        }
      });

      $(".add-to-cart").click(function () {
        const name = $(this).data("name");
        const price = parseFloat($(this).data("price"));
        const index = $(this).data("index");
        const quantity = parseInt($(`.quantity[data-index="${index}"]`).text());
        addToCart(index + 1, name, price, quantity);

        $(`#productModal-${index}`).modal('hide');
      });
    },
    error: function (xhr, status, error) {
      console.error("Error fetching menu items:", error);
    },
  });

  function addToCart(id, izena, prezioa, quantity) {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    const existingProductIndex = cart.findIndex((item) => item.id === id);

    if (existingProductIndex > -1) {
        cart[existingProductIndex].quantity += quantity;
    } else {
        cart.push({ id: id, name: izena, price: prezioa, quantity: quantity });
    }

    localStorage.setItem('cart', JSON.stringify(cart));

    const notification = $("#notification");
    notification.stop().fadeIn(300).delay(1000).fadeOut(300);
}
});
