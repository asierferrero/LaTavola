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

      // Produktuak nahastu eta lehenengo 3 aukeratu
      const randomItems = shuffle(data).slice(0, 3);

      randomItems.forEach(function (item) {
        $("#gomendioak").append(`
            <div class="recommended-item mb-3 d-flex flex-md-row flex-column align-items-center">
                <div class="recommended-img-container mb-2 mb-md-0">
                    <img src="${item.img}" class="img-fluid recommended-img" alt="${item.izena}">
                </div>
                <div class="recommended-text">
                    <h4>${item.izena}</h4>
                    <button class="btn btn-danger" onclick="addToCart('${item.izena}', ${item.prezioa})">Eskatu</button>
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

function addToCart(productName, productPrice) {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const existingProductIndex = cart.findIndex(
    (item) => item.name === productName
  );

  if (existingProductIndex > -1) {
    cart[existingProductIndex].quantity += 1;
  } else {
    cart.push({ name: productName, price: productPrice, quantity: 1 });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  displayCartItems();
}

function removeFromCart(productName) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart = cart.filter((item) => item.name !== productName);
  localStorage.setItem("cart", JSON.stringify(cart));
  displayCartItems();
}

function updateQuantity(productName, change) {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const product = cart.find((item) => item.name === productName);

  if (product) {
    product.quantity += change;
    if (product.quantity <= 0) {
      removeFromCart(productName);
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

function comprar() {
  localStorage.removeItem("cart");
  displayCartItems();
  window.location.href = "{% url 'order_confirmation' %}"; 
}

document.addEventListener("DOMContentLoaded", displayCartItems);
