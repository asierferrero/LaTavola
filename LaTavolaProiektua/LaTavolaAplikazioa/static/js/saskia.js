$(document).ready(function () {
  $.ajax({
    url: "/api/produktuak/",
    method: "GET",
    success: function (data) {
      function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
      }

      // Produktuak nahastu eta lehenengo 4 aukeratu
      const randomItems = shuffle(data).slice(0, 4);

      randomItems.forEach(function (item) {
        $("#gomendioak").append(`
            <div class="recommended-item mb-3 d-flex flex-md-row flex-column align-items-center">
                <div class="recommended-img-container mb-2 mb-md-0">
                    <img src="${item.img}" class="img-fluid recommended-img" alt="${item.izena}">
                </div>
                <div class="recommended-text">
                    <h4>${item.izena}</h4>
                    <button class="btn btn-danger" onclick="addToCart('${item.id}', '${item.izena}', ${item.prezioa})">Eskatu</button>
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

function addToCart(id, izena, prezioa) {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const existingProductIndex = cart.findIndex(
    (item) => item.name === izena
  );

  if (existingProductIndex > -1) {
    cart[existingProductIndex].quantity += 1;
  } else {
    cart.push({ id: id, name: izena, price: prezioa, quantity: 1 });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  displayCartItems();
}

function removeFromCart(izena) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart = cart.filter((item) => item.name !== izena);
  localStorage.setItem("cart", JSON.stringify(cart));
  displayCartItems();
}

function updateQuantity(izena, change) {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const product = cart.find((item) => item.name === izena);

  if (product) {
    product.quantity += change;
    if (product.quantity <= 0) {
      removeFromCart(izena);
    } else {
      localStorage.setItem("cart", JSON.stringify(cart));
      displayCartItems();
    }
  }
}

function displayCartItems() {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const cartItemsContainer = document.getElementById("cartItems");
  const totalPriceElement = document.getElementById("totalPrice");

  cartItemsContainer.innerHTML = "";
  let total = 0;

  cart.forEach((item) => {
    const itemElement = document.createElement("div");
    itemElement.classList.add(
      "cart-item",
      "d-flex",
      "align-items-center",
      "justify-content-between",
      "p-2",
      "border",
      "mb-2",
      "rounded"
    );
    itemElement.innerHTML = `
        <span>${item.name}</span>
       <!-- En el HTML del item en el carrito -->
        <div class="cart-item-buttons">
          <button class="btn btn-danger btn-small" onclick="removeFromCart('${
            item.name
          }')">🗑️</button>
          <button class="btn btn-secondary btn-small" onclick="updateQuantity('${
            item.name
          }', -1)">-</button>
          <span>${item.quantity}x</span>
          <button class="btn btn-secondary btn-small" onclick="updateQuantity('${
            item.name
          }', 1)">+</button>
        </div>
        <span class="price">${(item.price * item.quantity).toFixed(2)}€</span>
        </div>
      `;
    cartItemsContainer.appendChild(itemElement);
    total += item.price * item.quantity;
  });

  totalPriceElement.innerHTML = `${total.toFixed(2)}€`;
}

document.addEventListener("DOMContentLoaded", displayCartItems);
