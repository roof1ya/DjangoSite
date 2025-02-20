// JavaScript for Craft Beer Store

// Function to update the store based on the selected switch
function updateStore() {
    const storeSwitch = document.getElementById('store-switch');
    const selectedStore = storeSwitch.value;

    // Fetch products for the selected store (simulation for now)
    const products = getProducts(selectedStore);

    // Update the product grid
    const productGrid = document.getElementById('product-grid');
    productGrid.innerHTML = '';

    products.forEach(product => {
        const productTile = document.createElement('div');
        productTile.classList.add('product-tile');

        productTile.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>Алкоголь: ${product.alcohol}%</p>
            <p>Горечь: ${product.bitterness} IBU</p>
            <p>Цена: ${product.price} руб.</p>
        `;

        productGrid.appendChild(productTile);
    });
}

// Simulated function to fetch products based on the selected store
function getProducts(store) {
    const sampleProducts = {
        store1: [
            { name: 'IPA Classic', alcohol: 6.5, bitterness: 50, price: 300, image: 'https://via.placeholder.com/150' },
            { name: 'Stout Dark', alcohol: 7.2, bitterness: 40, price: 350, image: 'https://via.placeholder.com/150' }
        ],
        store2: [
            { name: 'Pilsner Light', alcohol: 5.0, bitterness: 20, price: 280, image: 'https://via.placeholder.com/150' },
            { name: 'Amber Ale', alcohol: 5.8, bitterness: 30, price: 320, image: 'https://via.placeholder.com/150' }
        ]
    };

    return sampleProducts[store] || [];
}

// Initialize the store on page load
window.onload = function() {
    updateStore();
};
