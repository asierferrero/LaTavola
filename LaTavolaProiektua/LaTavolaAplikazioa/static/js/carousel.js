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
  
      const randomItems = shuffle(data);
      $('#carouselItems').empty();
      $('.carousel-indicators').empty();
  
      for (let i = 0; i < randomItems.length; i += 5) {
        const items = randomItems.slice(i, i + 5);
        const slideClass = i === 0 ? 'carousel-item active' : 'carousel-item';
        const carouselSlide = `
          <div class="${slideClass}">
            <div class="row" style="display: flex; justify-content: space-between;">
              ${items.map(item => `
                <div class="carousel-item-content" style="flex: 1; padding: 0 5px;">
                  <img src="${item.img}" class="d-block w-100" alt="${item.name}">
                </div>
              `).join('')}
            </div>
          </div>
        `;
  
        $('#carouselItems').append(carouselSlide);
  
        const indicatorClass = i === 0 ? 'active' : '';
        const indicator = `<button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="${i / 5}" class="carousel-indicator ${indicatorClass}" aria-current="true" aria-label="Slide ${i / 5 + 1}"></button>`;
        $('.carousel-indicators').append(indicator);
      }
  
      $('#carouselExampleIndicators').carousel({
        interval: 2500,
        ride: 'carousel',
        wrap: true
      });
    },
    error: function (error) {
      console.error("Error al obtener los productos:", error);
    }
  });
  