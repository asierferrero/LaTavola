function calcularTotal() {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  return cart.reduce((total, item) => total + item.price * item.quantity, 0).toFixed(2);
}

function erosi() {
  const total = calcularTotal();
  document.getElementById("total").value = total;
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError)
  } else {
    alert('Geolokalizazioa ez da onartzen zure arakatzailean.')
  }
}

function showPosition(position) {
  const lat = position.coords.latitude
  const lon = position.coords.longitude
  const geolocationAPI = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`

  fetch(geolocationAPI)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('address').value = data.display_name
    })
    .catch((error) => {
      alert('Errore bat gertatu da kokapena eskuratzean.')
      console.error('Error fetching address:', error)
    })
}

function showError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      alert('Kokapena lortzeko baimena ukatu da.')
      break
    case error.POSITION_UNAVAILABLE:
      alert('Kokapena ezin da eskuratu.')
      break
    case error.TIMEOUT:
      alert('Kokapena lortzeko denbora amaitu da.')
      break
    default:
      alert('Errore ezezaguna.')
      break
  }
}