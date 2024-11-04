$(document).ready(function () {
    $.ajax({
        url: "/saskia/",
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
                            <p>${item.deskripzioa}</p>
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
