$(document).ready(function () {
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
              alert(
                "Ocurrió un error al actualizar el stock. Inténtalo nuevamente."
              );
            },
          });
        }
      },
      error: function (xhr, status, error) {
        console.error("Error al actualizar el stock:", error);
        console.error("Detalles de la respuesta:", xhr.responseText);
        alert("Ocurrió un error al actualizar el stock. Inténtalo nuevamente.");
      },
    });
  });

  localStorage.removeItem("cart");
});
