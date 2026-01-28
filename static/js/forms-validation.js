/**
 * Form Validation and Enhancement Script
 * Adiciona validações client-side e melhorias de UX aos formulários
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar validações
    initializeFormValidation();
    initializeDateTimePickers();
    initializeToasts();
});

/**
 * Inicializa validação de formulários Bootstrap
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                showToast('Por favor, preencha todos os campos obrigatórios corretamente.', 'warning');
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Inicializa seletores de data e hora
 */
function initializeDateTimePickers() {
    // Encontrar todos os campos de data e hora
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const timeInputs = document.querySelectorAll('input[type="time"]');
    const dateTimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    
    // Adicionar classe CSS para estilização
    dateInputs.forEach(input => {
        input.classList.add('form-control', 'date-picker');
        input.setAttribute('required', 'required');
    });
    
    timeInputs.forEach(input => {
        input.classList.add('form-control', 'time-picker');
        input.setAttribute('required', 'required');
    });
    
    dateTimeInputs.forEach(input => {
        input.classList.add('form-control', 'datetime-picker');
        input.setAttribute('required', 'required');
    });
    
    // Validar datas (não permitir datas passadas para agendamentos)
    document.querySelectorAll('input[data-type="appointment-date"]').forEach(input => {
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                showToast('Não é possível agendar para datas passadas.', 'danger');
                this.value = '';
            }
        });
    });
}

/**
 * Sistema de Toast Notifications
 */
function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto-dismiss após 5 segundos
    setTimeout(() => {
        const toastElement = document.getElementById(toastId);
        if (toastElement) {
            toastElement.remove();
        }
    }, 5000);
}

/**
 * Obter ou criar container de toasts
 */
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }
    
    return container;
}

/**
 * Inicializar toasts
 */
function initializeToasts() {
    const toastElements = document.querySelectorAll('.alert');
    toastElements.forEach(element => {
        // Remover alertas após 5 segundos
        setTimeout(() => {
            element.style.opacity = '0';
            setTimeout(() => {
                element.remove();
            }, 300);
        }, 5000);
    });
}

/**
 * Validar CPF
 */
function validateCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
        return false;
    }
    
    let sum = 0;
    let remainder;
    
    for (let i = 1; i <= 9; i++) {
        sum += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.substring(9, 10))) return false;
    
    sum = 0;
    for (let i = 1; i <= 10; i++) {
        sum += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.substring(10, 11))) return false;
    
    return true;
}

/**
 * Validar Email
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validar Telefone
 */
function validatePhone(phone) {
    const re = /^(\d{2})\s?(\d{4,5})-?(\d{4})$/;
    return re.test(phone.replace(/\D/g, ''));
}

/**
 * Confirmar ação destrutiva
 */
function confirmAction(message = 'Tem certeza que deseja continuar?') {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirmação</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${message}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-danger" id="confirm-btn">Confirmar</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        
        document.getElementById('confirm-btn').addEventListener('click', () => {
            bsModal.hide();
            modal.remove();
            resolve(true);
        });
        
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
            resolve(false);
        });
        
        bsModal.show();
    });
}
