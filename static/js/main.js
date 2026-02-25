// Main JavaScript file for Promptuario

// Auto-hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Menu toggle functionality
    const menuToggle = document.getElementById('menu-toggle');
    const asideMenu = document.querySelector('.aside-menu');

    if (menuToggle && asideMenu) {
        menuToggle.addEventListener('click', function() {
            asideMenu.classList.toggle('open');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!asideMenu.contains(event.target) && !menuToggle.contains(event.target)) {
                asideMenu.classList.remove('open');
            }
        });
    }
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Tem certeza que deseja excluir este item?');
}

// Format CPF input
function formatCPF(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length <= 11) {
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    input.value = value;
}

// Format phone input
function formatPhone(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length <= 11) {
        value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
        value = value.replace(/(\d)(\d{4})$/, '$1-$2');
    }
    input.value = value;
}

// Format CEP input
function formatCEP(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length <= 8) {
        value = value.replace(/^(\d{5})(\d)/, '$1-$2');
    }
    input.value = value;
}
