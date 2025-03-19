// Main JavaScript file 
// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Toggle FAQ answers
    const faqQuestions = document.querySelectorAll('.faq-question');
    if (faqQuestions) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', function() {
                this.classList.toggle('active');
                const answer = this.nextElementSibling;
                if (answer.style.display === 'block') {
                    answer.style.display = 'none';
                } else {
                    answer.style.display = 'block';
                }
            });
        });
    }
    
    // Product quantity selector
    const quantityInput = document.querySelector('.quantity-input');
    const incrementBtn = document.querySelector('.increment-btn');
    const decrementBtn = document.querySelector('.decrement-btn');
    
    if (quantityInput && incrementBtn && decrementBtn) {
        incrementBtn.addEventListener('click', function() {
            let value = parseInt(quantityInput.value);
            const max = parseInt(quantityInput.getAttribute('max'));
            value = isNaN(value) ? 1 : value;
            
            if (value < max) {
                value++;
                quantityInput.value = value;
            }
        });
        
        decrementBtn.addEventListener('click', function() {
            let value = parseInt(quantityInput.value);
            value = isNaN(value) ? 1 : value;
            
            if (value > 1) {
                value--;
                quantityInput.value = value;
            }
        });
    }
    
    // Dropdown filters
    const filterOptions = document.querySelectorAll('.dropdown-item');
    if (filterOptions) {
        filterOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                e.preventDefault();
                const filterText = this.textContent;
                const dropdownButton = this.closest('.dropdown').querySelector('.dropdown-toggle');
                dropdownButton.textContent = 'Sắp xếp theo: ' + filterText;
            });
        });
    }
    
    // Image zoom effect on product detail
    const productImage = document.querySelector('.product-image img');
    if (productImage) {
        productImage.addEventListener('mousemove', function(e) {
            const x = e.clientX - e.target.offsetLeft;
            const y = e.clientY - e.target.offsetTop;
            
            const imgWidth = e.target.offsetWidth;
            const imgHeight = e.target.offsetHeight;
            
            const xPercent = x / imgWidth * 100;
            const yPercent = y / imgHeight * 100;
            
            e.target.style.transformOrigin = `${xPercent}% ${yPercent}%`;
            e.target.style.transform = 'scale(1.5)';
        });
        
        productImage.addEventListener('mouseleave', function() {
            productImage.style.transformOrigin = 'center center';
            productImage.style.transform = 'scale(1)';
        });
    }
    
    // Cart item quantity update
    const cartItemQuantity = document.querySelectorAll('.cart-item-quantity');
    if (cartItemQuantity) {
        cartItemQuantity.forEach(item => {
            item.addEventListener('change', function() {
                this.closest('form').submit();
            });
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    if (forms) {
        Array.prototype.slice.call(forms).forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    }
});