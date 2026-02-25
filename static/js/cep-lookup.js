/**
 * CEP Lookup Script
 * Busca automática de endereço via CEP usando API ViaCEP
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeCepLookup();
});

/**
 * Inicializar busca de CEP
 */
function initializeCepLookup() {
    const cepInputs = document.querySelectorAll('[data-lookup="cep"]');
    
    cepInputs.forEach(input => {
        // Event listener para blur (quando o usuário sai do campo)
        input.addEventListener('blur', function() {
            if (this.value.length >= 8) {
                performCepLookup(this);
            }
        });

        // Permitir busca ao pressionar Enter
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && this.value.length >= 8) {
                e.preventDefault();
                performCepLookup(this);
            }
        });

        // Formatar CEP enquanto digita
        input.addEventListener('input', function() {
            this.value = formatCep(this.value);
        });
    });
}

/**
 * Formatar CEP (XX.XXX-XXX)
 */
function formatCep(value) {
    value = value.replace(/\D/g, '');
    if (value.length > 5) {
        value = value.slice(0, 5) + '-' + value.slice(5, 8);
    }
    return value;
}

/**
 * Realizar busca de CEP
 */
function performCepLookup(input) {
    const cep = input.value.replace(/\D/g, '');
    
    if (cep.length !== 8) {
        showCepError(input, 'CEP deve conter 8 dígitos');
        return;
    }

    // Mostrar loading
    showCepLoading(input);

    // Fazer requisição à API ViaCEP
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            if (data.erro) {
                showCepError(input, 'CEP não encontrado');
                clearAddressFields(input);
            } else {
                fillAddressFields(input, data);
                showCepSuccess(input);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar CEP:', error);
            showCepError(input, 'Erro ao buscar CEP. Tente novamente.');
        });
}

/**
 * Preencher campos de endereço
 */
function fillAddressFields(cepInput, data) {
    const form = cepInput.closest('form');
    if (!form) return;

    // Mapear campos de endereço
    const fieldMappings = {
        'logradouro': ['address', 'street', 'rua', 'endereco'],
        'bairro': ['neighborhood', 'bairro', 'district'],
        'localidade': ['city', 'cidade', 'municipio'],
        'uf': ['state', 'estado', 'uf', 'provincia']
    };

    // Preencher cada campo
    Object.entries(fieldMappings).forEach(([cepField, possibleNames]) => {
        const value = data[cepField] || '';
        
        // Procurar pelo campo no formulário
        possibleNames.forEach(name => {
            const field = form.querySelector(`input[name*="${name}"], input[id*="${name}"]`);
            if (field) {
                field.value = value;
                field.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    });

    // Focar no próximo campo (número)
    const numberField = form.querySelector('input[name*="number"], input[id*="number"], input[name*="numero"]');
    if (numberField) {
        numberField.focus();
    }
}

/**
 * Limpar campos de endereço
 */
function clearAddressFields(cepInput) {
    const form = cepInput.closest('form');
    if (!form) return;

    const addressFields = form.querySelectorAll('input[name*="address"], input[name*="street"], input[name*="rua"], input[name*="endereco"], input[name*="neighborhood"], input[name*="bairro"], input[name*="city"], input[name*="cidade"], input[name*="state"], input[name*="estado"], input[name*="uf"]');
    
    addressFields.forEach(field => {
        field.value = '';
    });
}

/**
 * Mostrar feedback de loading
 */
function showCepLoading(input) {
    removeCepFeedback(input);
    
    const feedback = document.createElement('div');
    feedback.className = 'cep-feedback loading';
    feedback.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Buscando endereço...';
    input.parentNode.appendChild(feedback);
    
    input.classList.add('is-loading');
}

/**
 * Mostrar feedback de sucesso
 */
function showCepSuccess(input) {
    removeCepFeedback(input);
    
    const feedback = document.createElement('div');
    feedback.className = 'cep-feedback success';
    feedback.innerHTML = '<i class="fas fa-check-circle"></i> Endereço encontrado com sucesso!';
    input.parentNode.appendChild(feedback);
    
    input.classList.add('is-valid');
    input.classList.remove('is-loading');
    
    // Remover feedback após 3 segundos
    setTimeout(() => {
        feedback.remove();
        input.classList.remove('is-valid');
    }, 3000);
}

/**
 * Mostrar feedback de erro
 */
function showCepError(input, message) {
    removeCepFeedback(input);
    
    const feedback = document.createElement('div');
    feedback.className = 'cep-feedback error';
    feedback.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    input.parentNode.appendChild(feedback);
    
    input.classList.add('is-invalid');
    input.classList.remove('is-loading');
}

/**
 * Remover feedback anterior
 */
function removeCepFeedback(input) {
    const existingFeedback = input.parentNode.querySelector('.cep-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    input.classList.remove('is-loading', 'is-valid', 'is-invalid');
}
