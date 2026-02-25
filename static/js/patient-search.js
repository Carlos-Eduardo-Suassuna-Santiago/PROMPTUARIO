/**
 * Patient Search Script
 * Implementa busca dinâmica de pacientes com AJAX
 */

document.addEventListener('DOMContentLoaded', function() {
    initializePatientSearch();
});

/**
 * Inicializar busca de pacientes
 */
function initializePatientSearch() {
    const searchInputs = document.querySelectorAll('[data-search="patient"]');
    
    searchInputs.forEach(input => {
        const resultsContainer = input.nextElementSibling;
        if (!resultsContainer || !resultsContainer.classList.contains('search-results')) {
            // Criar container de resultados se não existir
            const container = document.createElement('div');
            container.className = 'search-results';
            input.parentNode.insertBefore(container, input.nextSibling);
        }

        // Event listeners
        input.addEventListener('input', debounce(function() {
            performPatientSearch(input);
        }, 300));

        input.addEventListener('focus', function() {
            if (this.value.length > 0) {
                performPatientSearch(this);
            }
        });

        // Fechar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (e.target !== input && !e.target.closest('.search-results')) {
                const results = input.parentNode.querySelector('.search-results');
                if (results) {
                    results.style.display = 'none';
                }
            }
        });
    });
}

/**
 * Realizar busca de pacientes
 */
function performPatientSearch(input) {
    const query = input.value.trim();
    const resultsContainer = input.parentNode.querySelector('.search-results');
    
    if (query.length < 2) {
        resultsContainer.style.display = 'none';
        return;
    }

    // Mostrar loading
    resultsContainer.innerHTML = '<div class="search-loading"><i class="fas fa-spinner fa-spin"></i> Buscando...</div>';
    resultsContainer.style.display = 'block';

    // Fazer requisição AJAX
    fetch(`/patients/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na busca');
            }
            return response.json();
        })
        .then(data => {
            displayPatientResults(resultsContainer, data, input);
        })
        .catch(error => {
            console.error('Erro ao buscar pacientes:', error);
            resultsContainer.innerHTML = '<div class="search-error">Erro ao buscar pacientes. Tente novamente.</div>';
        });
}

/**
 * Exibir resultados da busca
 */
function displayPatientResults(container, patients, input) {
    if (patients.length === 0) {
        container.innerHTML = '<div class="search-empty">Nenhum paciente encontrado.</div>';
        return;
    }

    let html = '<div class="search-items">';
    
    patients.forEach(patient => {
        html += `
            <div class="search-item" data-patient-id="${patient.id}">
                <div class="search-item-main">
                    <strong>${escapeHtml(patient.name)}</strong>
                    <small class="text-muted d-block">${escapeHtml(patient.cpf)}</small>
                </div>
                <div class="search-item-meta">
                    <small class="text-muted">${escapeHtml(patient.email)}</small>
                </div>
            </div>
        `;
    });

    html += '</div>';
    container.innerHTML = html;

    // Adicionar event listeners aos itens
    container.querySelectorAll('.search-item').forEach(item => {
        item.addEventListener('click', function() {
            selectPatient(this, input);
        });
    });
}

/**
 * Selecionar paciente
 */
function selectPatient(element, input) {
    const patientId = element.dataset.patientId;
    const patientName = element.querySelector('strong').textContent;
    
    // Atualizar input
    input.value = patientName;
    
    // Atualizar campo oculto (se existir)
    const hiddenField = input.parentNode.querySelector('input[type="hidden"]');
    if (hiddenField) {
        hiddenField.value = patientId;
    }
    
    // Fechar resultados
    const resultsContainer = input.parentNode.querySelector('.search-results');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
    }
    
    // Disparar evento customizado
    input.dispatchEvent(new CustomEvent('patientSelected', {
        detail: { id: patientId, name: patientName }
    }));
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Escapar HTML para evitar XSS
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
