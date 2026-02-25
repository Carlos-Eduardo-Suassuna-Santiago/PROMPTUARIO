/**
 * Loading States Script
 * Gerencia estados de carregamento e feedback visual
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeLoadingStates();
});

/**
 * Inicializar loading states
 */
function initializeLoadingStates() {
    // Adicionar loading state ao submeter formulários
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !this.classList.contains('no-loading')) {
                addLoadingState(submitBtn);
            }
        });
    });

    // Adicionar loading state a links com classe 'btn-loading'
    document.querySelectorAll('a.btn-loading').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.classList.contains('disabled')) {
                addLoadingState(this);
            }
        });
    });
}

/**
 * Adicionar loading state a um elemento
 */
function addLoadingState(element) {
    if (element.classList.contains('loading')) {
        return; // Já está em loading
    }

    element.classList.add('loading');
    element.disabled = true;

    // Armazenar conteúdo original
    const originalContent = element.innerHTML;
    element.dataset.originalContent = originalContent;

    // Mostrar spinner
    const spinner = document.createElement('span');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    element.innerHTML = '';
    element.appendChild(spinner);

    // Adicionar texto de loading
    const text = document.createElement('span');
    text.className = 'loading-text';
    text.textContent = element.dataset.loadingText || 'Carregando...';
    element.appendChild(text);
}

/**
 * Remover loading state de um elemento
 */
function removeLoadingState(element) {
    if (!element.classList.contains('loading')) {
        return;
    }

    element.classList.remove('loading');
    element.disabled = false;
    element.innerHTML = element.dataset.originalContent || 'Enviar';
}

/**
 * Mostrar toast notification
 */
function showToast(message, type = 'info', duration = 5000) {
    const toastContainer = getOrCreateToastContainer();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    const iconMap = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };

    const icon = iconMap[type] || 'info-circle';

    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${icon}"></i>
            <span class="toast-message">${escapeHtml(message)}</span>
        </div>
        <button type="button" class="toast-close" aria-label="Fechar">
            <i class="fas fa-times"></i>
        </button>
    `;

    toastContainer.appendChild(toast);

    // Adicionar event listener ao botão de fechar
    toast.querySelector('.toast-close').addEventListener('click', function() {
        removeToast(toast);
    });

    // Auto-remover após duração
    if (duration > 0) {
        setTimeout(() => {
            removeToast(toast);
        }, duration);
    }

    return toast;
}

/**
 * Remover toast
 */
function removeToast(toast) {
    toast.classList.add('removing');
    setTimeout(() => {
        toast.remove();
    }, 300);
}

/**
 * Obter ou criar container de toasts
 */
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    return container;
}

/**
 * Mostrar modal de confirmação
 */
function showConfirmModal(title, message, onConfirm, onCancel) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'confirmModal';
    modal.setAttribute('tabindex', '-1');
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${escapeHtml(title)}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    ${escapeHtml(message)}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-primary" id="confirmBtn">Confirmar</button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();

    document.getElementById('confirmBtn').addEventListener('click', function() {
        bsModal.hide();
        if (typeof onConfirm === 'function') {
            onConfirm();
        }
    });

    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
        if (typeof onCancel === 'function') {
            onCancel();
        }
    });

    return bsModal;
}

/**
 * Escapar HTML
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Mostrar loading overlay na página
 */
function showPageLoading(message = 'Carregando...') {
    const overlay = document.createElement('div');
    overlay.id = 'page-loading-overlay';
    overlay.className = 'page-loading-overlay';
    overlay.innerHTML = `
        <div class="page-loading-content">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
            <p class="mt-3">${escapeHtml(message)}</p>
        </div>
    `;

    document.body.appendChild(overlay);
    return overlay;
}

/**
 * Remover loading overlay
 */
function hidePageLoading() {
    const overlay = document.getElementById('page-loading-overlay');
    if (overlay) {
        overlay.classList.add('removing');
        setTimeout(() => {
            overlay.remove();
        }, 300);
    }
}
