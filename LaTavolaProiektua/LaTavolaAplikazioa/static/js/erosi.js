function removeFromCart(id) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  // Filtrar el carrito usando el ID del producto
  cart = cart.filter((item) => item.id !== id);
  localStorage.setItem("cart", JSON.stringify(cart));
  displayCartItems();
}

function updateQuantity(id, change) {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  const product = cart.find((item) => item.id === id);

  if (product) {
    product.quantity += change;
    if (product.quantity <= 0) {
      removeFromCart(id);
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
          <div class="cart-item-buttons">
            <button class="btn btn-danger btn-small" onclick="removeFromCart(${item.id})">🗑️</button>
            <button class="btn btn-secondary btn-small" onclick="updateQuantity(${item.id}, -1)">-</button>
            <span>${item.quantity}x</span>
            <button class="btn btn-secondary btn-small" onclick="updateQuantity(${item.id}, 1)">+</button>
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

function erosi() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    
    cart.forEach((item) => {
      const id = item.id;
      const name = item.name;   
      const price = item.price;
      const quantity = item.quantity;
  
      $.ajax({
        url: `/api/produktuak/${id}/`,
        method: "GET",
        success: function (response) {
          const currentStock = response.stock;
  
          if (currentStock >= quantity) {
            const newStock = currentStock - quantity;
  
            $.ajax({
              url: `/api/produktuak/${id}/`,
              method: "PUT",
              contentType: "application/json",
              data: JSON.stringify({
                izena: name,
                prezioa: price,
                stock: newStock,
              }),
              success: function () {
                console.log("Stock actualizado correctamente.");
              },
              error: function (xhr, status, error) {
                console.error("Error al actualizar el stock:", error);
                alert("Ocurrió un error al actualizar el stock. Inténtalo nuevamente.");
              }
            });
          } else {
            alert(`No hay suficiente stock para el producto ${name}.`);
          }
        },
        error: function (xhr, status, error) {
          console.error("Error al obtener el stock actual:", error);
          alert("Ocurrió un problema al verificar el stock del producto. Inténtalo nuevamente.");
        },
      });
    });
  
    localStorage.removeItem("cart");
    displayCartItems();
  }
  
