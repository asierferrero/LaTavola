function produktuenGrafikoa(nombres, stock, precios) {
    const ctx = document.getElementById('graficoProductos').getContext('2d');
  
    const graficoProductos = new Chart(ctx, {
      type: 'bar', // Tipo de gráfico (barras)
      data: {
        labels: nombres, // Etiquetas para cada barra (nombres de los productos)
        datasets: [{
          label: 'Produktuen Stocka',
          data: stock, // Valores de stock
          backgroundColor: 'rgba(75, 192, 192, 0.5)', // Color de las barras de stock
          borderColor: 'rgba(75, 192, 192, 1)', // Color de los bordes de las barras
          borderWidth: 1
        }, {
          label: 'Produktuen prezioak',
          data: precios, // Valores de precios
          backgroundColor: 'rgba(255, 99, 132, 0.5)', // Color de las barras de precios
          borderColor: 'rgba(255, 99, 132, 1)', // Color de los bordes de las barras
          borderWidth: 1
        }]
      },
      options: {
        responsive: true, // Hace que el gráfico sea responsivo
        scales: {
          y: {
            beginAtZero: true // Hace que el eje Y empiece desde 0
          }
        }
      }
    });
  }
  