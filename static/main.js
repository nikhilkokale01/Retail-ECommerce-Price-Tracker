// document.addEventListener("DOMContentLoaded", function() {
//     // Add event listener to product select dropdown
//     document.getElementById("productSelect").addEventListener("change", function() {
//         var productId = this.value;
//         if (productId !== "0") {
//             fetchProductDetails(productId);
//             //fetchPriceDetails(productId);
//         } else {
//             clearProductDetails();
//             //clearPriceDetails(); 
//         }
//     });

//     // Add event listener to product image
//     var productImage = document.getElementById("productImage");
//     if(productImage) {
//         productImage.addEventListener("click", function() {
//             console.log("Product image clicked");
//             var productId = document.getElementById("productSelect").value;
//             if (productId !== "0") {
//                 console.log(productId);
//                 fetchPriceDetails(productId);
//             }
//         });
//     } else {
//         console.log("Product image element not found");
//     }

//     document.getElementById("add_to_wishlist_button").addEventListener("click", function() {
//         var productId = document.getElementById("productSelect").value;
//         if (productId !== "0") {
//             addProductToWishlist(productId);
//         }
//     });

// });

// document.addEventListener("DOMContentLoaded", function() {
//     document.querySelector('.product-details').style.display = "none";

//     // Add event listener to navbar items
//     var navbarItems = document.querySelectorAll('.categories a');
//     navbarItems.forEach(function(item) {
//         item.addEventListener("click", function() {
//             var category = item.getAttribute("value");
//             console.log("Category selected:", category);
//             fetchProducts(category);

//             // Show the select product part
//             document.querySelector('.dropdown').style.display = "block";
//         });
//     });


//     // Add event listener to product select dropdown
//     document.getElementById("productSelect").addEventListener("change", function() {
//         var productId = this.value;
//         if (productId !== "0") {
//             fetchProductDetails(productId);
//             // Show add to wishlist button after selecting a product
//             document.getElementById("add_to_wishlist_button").style.display = 'block';
//         } else {
//             clearProductDetails();
//         }
//     });

//     // Add event listener to add to wishlist button
//     document.getElementById("add_to_wishlist_button").addEventListener("click", function() {
//         var productId = document.getElementById("productSelect").value;
//         if (productId !== "0") {
//             addProductToWishlist(productId);
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", function() {
    // Hide product details initially
    document.querySelector('.product-details').style.display = "none";
    document.querySelector('.price-details').style.display = "none";
    document.querySelector('.card').style.display = "none";


    // Add event listener to navbar items
    var navbarItems = document.querySelectorAll('.categories a');
    navbarItems.forEach(function(item) {
        item.addEventListener("click", function() {
            var category = item.getAttribute("value");
            console.log("Category selected:", category);
            fetchProducts(category);

            // Show the select product part
            document.querySelector('.dropdown').style.display = "block";
        });
    });

    // Add event listener to product select dropdown
    document.getElementById("productSelect").addEventListener("change", function() {
        var productId = this.value;
        if (productId !== "0") {
            document.querySelector('.card').style.display = "block";

            fetchProductDetails(productId);
            // Show product details after selecting a product
            document.querySelector('.product-details').style.display = "block";
            fetchPriceDetails(productId);
            // Show price details after selecting a product
            document.querySelector('.price-details').style.display = "block";
        } else {
            clearProductDetails();
            clearPriceDetails();
            // Hide product and price details if no product is selected
            document.querySelector('.card').style.display = "none";

            document.querySelector('.product-details').style.display = "none";
            document.querySelector('.price-details').style.display = "none";
        }
    });

    // Add event listener to add to wishlist button
    document.getElementById("add_to_wishlist_button").addEventListener("click", function() {
        var productId = document.getElementById("productSelect").value;
        if (productId !== "0") {
            addProductToWishlist(productId);
        }
    });
});

// Function to add product to wishlist
function addProductToWishlist(productId) {
    // Make an AJAX request to add product to wishlist
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_to_watchlist/" + productId, true);
    xhr.setRequestHeader("Content-Type", "application/json");
   
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log("Product added to wishlist successfully!");
                alert("Product added to wishlist successfully!");
            } else {
                console.error("Failed to add product to wishlist. Status:", xhr.status);
                alert("Failed to add product to wishlist. Please try again.");
            }
        }
    };
    xhr.send();
}


function fetchProductDetails(productId) {
    // AJAX request to fetch product details
    // toggleActiveClass(category.toLowerCase() + 'Btn');

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/product/" + productId, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var product = JSON.parse(xhr.responseText);
            updateProductDetails(product);
        }
    };
    xhr.send();
}

function updateProductDetails(product) {
    // Update product description, brand, and image
    document.getElementById("productDescription").textContent = product.prod_description;
    document.getElementById("productBrand").textContent = product.brand;
    document.getElementById("productImage").src = product.image;
}

function clearProductDetails() {
    // Clear product details
    document.getElementById("productDescription").textContent = "N/A";
    document.getElementById("productBrand").textContent = "N/A";
    document.getElementById("productImage").src = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png";
}

function fetchProducts(category) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/products/" + category, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var products = JSON.parse(xhr.responseText);
            displayProducts(products);
        }
    };
    xhr.send();
}


function displayProducts(products) {
    var select = document.getElementById("productSelect");
    select.innerHTML = "<option value='0'>-- Select Product --</option>";
    products.forEach(function(product) {
        var option = document.createElement("option");
        option.value = product.product_id;
        option.text = product.prod_description; // Set option text to product description
        select.appendChild(option);
    });
}

function fetchPriceDetails(productId) {
    // AJAX request to fetch price details based on product ID
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/price/" + productId, true);
    xhr.onload = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var prices = JSON.parse(xhr.responseText);
            console.log(prices);
            
            updatePriceDetails(prices);
        }
    };
    xhr.send();
}

function updatePriceDetails(prices) {
    // Clear previous price details
    var priceTableBody = document.getElementById("priceTableBody");
    priceTableBody.innerHTML = "";

    // Update price details in the table
    prices.forEach(function(price) {
        var row = document.createElement("tr");
        row.innerHTML =
                        "<td>" + price.website + "</td>" +
                        "<td>" + "Rs."+price.Price + "</td>" +
                        "<td><a href='" + price.url + "' target='_blank'>Visit</a></td>";

        console.log(row);
        priceTableBody.appendChild(row);
    });
}

function clearPriceDetails() {
    // Clear price details
    var priceTableBody = document.getElementById("priceTableBody");
    priceTableBody.innerHTML = "";
}

//color change for buttons
function toggleActiveClass(btnId) {
    var buttons = document.querySelectorAll('.navbar a');
    buttons.forEach(function(btn) {
        if (btn.id === btnId) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// document.getElementById('add_to_wishlist_button').addEventListener('click', function() {
//         // Send an AJAX request to your Flask route
//     var xhr = new XMLHttpRequest();
//     xhr.open('GET', '/add_to_watchlist', true);
//     xhr.onload = function () {
//         if (xhr.status === 200) {
//             // Request was successful
//             console.log(xhr.responseText);
//         } else {
//             // Request failed
//             console.error('Request failed with status:', xhr.status);
//         }
//     };
//     xhr.onerror = function () {
//         // An error occurred during the request
//         console.error('Request failed');
//     };
//     xhr.send();
// });
// }
