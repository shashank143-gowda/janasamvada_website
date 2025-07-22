// JanSamvaad Main JavaScript

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    
    // Create toast container if it doesn't exist
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '5';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Toast content
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add toast to container
    document.getElementById('toast-container').appendChild(toast);
    
    // Initialize and show toast
    const toastElement = new bootstrap.Toast(document.getElementById(toastId), {
        autohide: true,
        delay: 5000
    });
    toastElement.show();
    
    // Remove toast after it's hidden
    document.getElementById(toastId).addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Get user's current location
function getCurrentLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const location = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                callback(location, null);
            },
            (error) => {
                callback(null, error.message);
            }
        );
    } else {
        callback(null, "Geolocation is not supported by this browser.");
    }
}

// Format date to YYYY-MM-DD
function formatDate(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Format date and time
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Truncate text with ellipsis
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

// Check if user is logged in
function isLoggedIn() {
    // This is a simple check - in a real app, you'd verify with the server
    return document.cookie.includes('session=');
}

// Upvote a hazard
function upvoteHazard(hazardId) {
    $.ajax({
        url: `/hazards/api/hazards/${hazardId}/upvote`,
        method: 'POST',
        success: function(response) {
            if (response.success) {
                // Update upvote count in UI
                const upvoteElement = document.getElementById(`upvote-count-${hazardId}`);
                if (upvoteElement) {
                    upvoteElement.textContent = response.upvotes;
                }
                showToast('Upvoted successfully!', 'success');
            } else {
                showToast(response.error || 'Failed to upvote', 'danger');
            }
        },
        error: function() {
            showToast('Failed to upvote. Please try again.', 'danger');
        }
    });
}

// Document ready
$(document).ready(function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Back to top button
    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn();
        } else {
            $('.back-to-top').fadeOut();
        }
    });
    
    $('.back-to-top').click(function() {
        $('html, body').animate({scrollTop: 0}, 800);
        return false;
    });
});