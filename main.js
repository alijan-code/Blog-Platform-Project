// Show/hide password functionality
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('togglePassword');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Image preview functionality
function previewImage(input) {
    const preview = document.getElementById('imagePreview');
    const previewContainer = document.getElementById('imagePreviewContainer');
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            previewContainer.style.display = 'block';
        }
        
        reader.readAsDataURL(input.files[0]);
    } else {
        previewContainer.style.display = 'none';
    }
}

// Confirm delete
function confirmDelete(postId) {
    if (confirm('Are you sure you want to delete this post?')) {
        document.getElementById('deleteForm' + postId).submit();
    }
}

// Auto-expanding textarea
function autoExpand(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

// Flash message auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 3000);
    });

    // Initialize auto-expanding textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', () => autoExpand(textarea));
        // Initial expansion
        autoExpand(textarea);
    });
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add loading indicator
function showLoading() {
    const loading = document.createElement('div');
    loading.className = 'loading-spinner';
    loading.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    document.body.appendChild(loading);
}

function hideLoading() {
    const loading = document.querySelector('.loading-spinner');
    if (loading) {
        loading.remove();
    }
}

// Add form submission handling
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.classList.contains('delete-form')) {
                showLoading();
            }
        });
    });
});
