$(document).ready(function () {
  $.ajax({
    url: "/api/produktuak/",
    method: "GET",
    success: function (data) {
      const ordena = ["Hasierakoa", "Lehena", "Bigarrena", "Gehigarria", "Postrea", "Kafea"];
      data.sort((a, b) => ordena.indexOf(a.mota) - ordena.indexOf(b.mota));

      let currentCategory = "";
      data.forEach(function (item, index) {
        if (item.mota !== currentCategory) {
          currentCategory = item.mota;
          if (currentCategory === 'Kafea') {
            $("#menu-items").append(`<div class="col-12 category-title ${currentCategory}"><h2>${currentCategory}k eta edatekoak</h2></div>`);
          } else {
            $("#menu-items").append(`<div class="col-12 category-title ${currentCategory}"><h2>${currentCategory}k</h2></div>`);
          }
        }

        let alergenoak = item.alergenoak.map(alergeno => `
          <img src="${alergeno.img}" style="width: 30px; height: 30px; margin-right: 5px" title="${alergeno.izena}" />
        `).join("");

        $("#menu-items").append(`
          <div class="col-12 col-md-3 menu-item ${item.mota}">
            <div class="card" data-bs-toggle="modal" data-bs-target="#productModal-${index}">
              <img src="${item.img}" alt="${item.izena}" class="card-img-top rounded" />
              <div class="card-body text-center">
                <h3 class="card-title">${item.izena} ${item.adin_nagusikoa ? `- <img src="${staticUrl}img/18.png" style="width: 20px; height: auto;" title='Adin nagusikoa' />` : ''}</h3>
                <p class="card-text">${item.deskripzioa}</p>
                <h4 class="card-price">${item.prezioa}€</h4>
              </div>
            </div>
          </div>
          
          <div class="modal fade" id="productModal-${index}" tabindex="-1" aria-labelledby="productModalLabel-${index}" aria-hidden="true">
            <div class="modal-dialog modal-lg">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">${item.izena}</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="row">
                    <div class="col-md-5">
                      <img src="${item.img}" class="img-fluid rounded" alt="${item.izena}" />
                    </div>
                    <div class="col-md-7">
                      <p>${item.deskripzioa}</p>
                      <div class="my-3">${alergenoak}</div>
                      <h4>${item.prezioa}€</h4>
                      <div class="quantity-controls">
                        <button class="btn btn-outline-secondary decrement" data-index="${index}">-</button>
                        <span class="quantity" data-index="${index}">1</span>
                        <button class="btn btn-outline-secondary increment" data-index="${index}" data-stock="${item.stock}">+</button>
                        <img src="${staticUrl}img/cart_negro.png" style="width: 35px;" alt="Add to Cart" class="add-to-cart" data-name="${item.izena}" data-price="${item.prezioa}" data-index="${index}" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `);
      });

      $(".filter-button").click(function () {
        const filterValue = $(this).data("filter");
        if (filterValue === "all") {
          $(".menu-item").show();
          $(".category-title").show();
        } else {
          $(".menu-item").hide();
          $(".category-title").hide();
          $(`.${filterValue}`).show();
        }
      });

      $(".increment").click(function () {
        const index = $(this).data("index");
        const stock = parseInt($(this).data("stock"));
        let quantityElement = $(`.quantity[data-index="${index}"]`);
        let quantity = parseInt(quantityElement.text());
        if (quantity < stock) quantityElement.text(quantity + 1);
      });

      $(".decrement").click(function () {
        const index = $(this).data("index");
        let quantityElement = $(`.quantity[data-index="${index}"]`);
        let quantity = parseInt(quantityElement.text());
        if (quantity > 1) quantityElement.text(quantity - 1);
      });

      $(".add-to-cart").click(function () {
        const name = $(this).data("name");
        const price = parseFloat($(this).data("price"));
        const index = $(this).data("index");
        const quantity = parseInt($(`.quantity[data-index="${index}"]`).text());
        addToCart(index + 1, name, price, quantity);
        $(`#productModal-${index}`).modal("hide");
      });
    },
    error: function (xhr, status, error) {
      console.error("Error fetching menu items:", error);
    },
  });

  function addToCart(id, izena, prezioa, quantity) {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const existingProductIndex = cart.findIndex((item) => item.id === id);
    if (existingProductIndex > -1) cart[existingProductIndex].quantity += quantity;
    else cart.push({ id: id, name: izena, price: prezioa, quantity: quantity });
    localStorage.setItem("cart", JSON.stringify(cart));
    $("#notification").stop().fadeIn(300).delay(1000).fadeOut(300);
  }
});
