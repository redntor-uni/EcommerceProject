//ADD TO CART FUNCTION UPON CLICK
function addToCart(id) {
  console.log(id)
  fetch(`/api/add_to_cart/${id}`, {
      method: 'POST',
      headers: {
              'Content-Type': 'application/json', // Specify JSON content type
              },
      body: JSON.stringify({})
  }).then(response => {
      window.location.href = "/Cart"
  }).catch(error => {
      console.error('There was a problem with the fetch operation:', error);
  })
}

//SEARCH FUNCTION USED ON INPUT. IF EMPTY RETURNS THE ORIGINAL PROMISE/ELSE RETURNS SEARCH
async function searchProducts() {
  const query = document.getElementById('search-input').value.trim();
  const resultsDiv = document.getElementById('product-container');
  if (query === '') {
      while (resultsDiv.firstChild) {
          resultsDiv.removeChild(resultsDiv.firstChild);
      }
      fetch('/api/Products')
        .then(response => response.json())
        .then(data => {
            const productContainer = document.getElementById('product-container');
            data.Products.forEach(Products => {
                let productDiv = document.createElement('div');
                productDiv.id = 'product-creation'
                productDiv.innerHTML = `
                    <div class="column product-img">
                        <h2>${Products.Name}</h2>
                        <img src="${Products.Img}" alt="${Products.ID}">
                        <p>Price: $${Products.Price}</p>
                        <button onclick="addToCart(${Products.ID})">Add to Cart</button>
                        </div>
                    <div class="column product-description">
                        <p>${Products.Description}</p>
                    </div>
                `;
                productContainer.appendChild(productDiv);
            });
        })
        .catch(error => console.log('Error:', error));
        return;
  } else {
      fetch(`/api/Products/search?query=${query}`)
          .then(response => response.json())
          .then(data => {
              resultsDiv.innerHTML = '';
              data.results.forEach(Products => {
                  let productDiv = document.createElement('div');
                  productDiv.id = 'product-creation'
                  productDiv.innerHTML = `
                    <div class="column product-img">
                        <h2>${Products.Name}</h2>
                        <img src="${Products.Img}" alt="${Products.ID}">
                        <p>Price: $${Products.Price}</p>
                        <button onclick="addToCart(${Products.ID})">Add to Cart</button>
                        </div>
                    <div class="column product-description">
                        <p>${Products.Description}</p>
                    </div>
                `;
                resultsDiv.appendChild(productDiv);
              });
          });
  }

}