/**
 * Profile Form Enhancements
 * Melhorias de UX e validação para o formulário de perfil
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================================================
    // 1. PREVIEW DE IMAGEM ANTES DO UPLOAD
    // ========================================================================
    
    const profilePhotoInput = document.querySelector('.profile-photo-upload input[type="file"]');
    const profileAvatar = document.querySelector('.profile-avatar');
    
    if (profilePhotoInput && profileAvatar) {
        profilePhotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            if (file) {
                // Validar tipo de arquivo
                if (!file.type.startsWith('image/')) {
                    alert('⚠️ Por favor, selecione um arquivo de imagem válido.');
                    e.target.value = '';
                    return;
                }
                
                // Validar tamanho (máximo 5MB)
                const maxSize = 5 * 1024 * 1024; // 5MB
                if (file.size > maxSize) {
                    alert('⚠️ A imagem não pode ser maior que 5MB.');
                    e.target.value = '';
                    return;
                }
                
                // Mostrar preview
                const reader = new FileReader();
                reader.onload = function(event) {
                    profileAvatar.style.opacity = '0.7';
                    profileAvatar.src = event.target.result;
                    
                    // Animação
                    setTimeout(() => {
                        profileAvatar.style.opacity = '1';
                        profileAvatar.style.transform = 'scale(1.05)';
                    }, 100);
                    
                    setTimeout(() => {
                        profileAvatar.style.transform = 'scale(1)';
                    }, 300);
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // ========================================================================
    // 2. VALIDAÇÃO DE CPF
    // ========================================================================
    
    const cpfInput = document.querySelector('input[name="cpf"]');
    
    if (cpfInput) {
        cpfInput.addEventListener('blur', function() {
            const cpf = this.value.replace(/\D/g, '');
            
            if (cpf.length === 11) {
                if (!isValidCPF(cpf)) {
                    this.style.borderColor = 'var(--danger-color)';
                    this.style.background = 'rgba(239, 68, 68, 0.05)';
                    addErrorMessage(this, 'CPF inválido');
                } else {
                    this.style.borderColor = 'var(--success-color)';
                    this.style.background = 'rgba(16, 185, 129, 0.05)';
                    removeErrorMessage(this);
                }
            }
        });
    }
    
    // ========================================================================
    // 3. MÁSCARA DE TELEFONE
    // ========================================================================
    
    const phoneInput = document.querySelector('input[name="phone"]');
    
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            
            if (value.length <= 2) {
                this.value = value;
            } else if (value.length <= 7) {
                this.value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
            } else {
                this.value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
            }
        });
    }
    
    // ========================================================================
    // 4. MÁSCARA DE CEP
    // ========================================================================
    
    const zipCodeInput = document.querySelector('input[name="zip_code"]');
    
    if (zipCodeInput) {
        zipCodeInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            
            if (value.length > 8) {
                value = value.slice(0, 8);
            }
            
            if (value.length <= 5) {
                this.value = value;
            } else {
                this.value = `${value.slice(0, 5)}-${value.slice(5)}`;
            }
        });
    }
    
    // ========================================================================
    // 5. VALIDAÇÃO DE EMAIL
    // ========================================================================
    
    const emailInput = document.querySelector('input[name="email"]');
    
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const email = this.value.trim();
            
            if (email && !isValidEmail(email)) {
                this.style.borderColor = 'var(--danger-color)';
                addErrorMessage(this, 'Email inválido');
            } else {
                this.style.borderColor = 'var(--border-color)';
                removeErrorMessage(this);
            }
        });
    }
    
    // ========================================================================
    // 6. DETECÇÃO DE MUDANÇAS NO FORMULÁRIO
    // ========================================================================
    
    const form = document.querySelector('.profile-update-container form');
    const submitButton = document.querySelector('.btn-save');
    let formChanged = false;
    
    if (form && submitButton) {
        // Capturar valores iniciais
        const initialValues = new FormData(form);
        
        form.addEventListener('change', function() {
            formChanged = true;
            submitButton.style.opacity = '1';
            submitButton.style.transform = 'translateY(0)';
        });
        
        form.addEventListener('submit', function(e) {
            submitButton.disabled = true;
            submitButton.classList.add('loading');
        });
        
        // Advertência ao tentar sair sem salvar
        window.addEventListener('beforeunload', function(e) {
            if (formChanged) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
    }
    
    // ========================================================================
    // 7. ANIMAÇÃO DE FOCO
    // ========================================================================
    
    const inputs = document.querySelectorAll('.form-group input, .form-group textarea, .form-group select');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });
    
    // ========================================================================
    // 8. ENTER PARA SUBMETER EM ALGUNS CAMPOS
    // ========================================================================
    
    const lastNameInput = document.querySelector('input[name="last_name"]');
    
    if (lastNameInput) {
        lastNameInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                form.submit();
            }
        });
    }
    
    // ========================================================================
    // 9. CONFIRMAÇÃO VISUAL DE DADOS
    // ========================================================================
    
    const birthDateInput = document.querySelector('input[name="birth_date"]');
    
    if (birthDateInput) {
        birthDateInput.addEventListener('change', function() {
            const date = new Date(this.value);
            const age = calculateAge(date);
            
            if (age >= 0 && age <= 150) {
                addSuccessMessage(this, `✓ ${age} anos`);
            } else {
                addErrorMessage(this, 'Data inválida');
            }
        });
    }
});

// ============================================================================
// FUNÇÕES UTILITÁRIAS
// ============================================================================

/**
 * Valida CPF usando algoritmo mod11
 */
function isValidCPF(cpf) {
    if (cpf.length !== 11) return false;
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
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
 * Valida email usando regex
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Calcula idade em anos
 */
function calculateAge(birthDate) {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    
    return age;
}

/**
 * Adiciona mensagem de erro visual
 */
function addErrorMessage(input, message) {
    removeErrorMessage(input);
    
    const errorElement = document.createElement('p');
    errorElement.className = 'text-danger';
    errorElement.textContent = message;
    input.parentElement.appendChild(errorElement);
}

/**
 * Adiciona mensagem de sucesso visual
 */
function addSuccessMessage(input, message) {
    removeErrorMessage(input);
    
    const successElement = document.createElement('p');
    successElement.style.color = 'var(--success-color)';
    successElement.style.fontSize = '0.8rem';
    successElement.style.fontWeight = '500';
    successElement.style.marginTop = '0.25rem';
    successElement.textContent = message;
    input.parentElement.appendChild(successElement);
}

/**
 * Remove mensagens de erro
 */
function removeErrorMessage(input) {
    const parent = input.parentElement;
    const messages = parent.querySelectorAll('.text-danger, p[style*="success"]');
    messages.forEach(msg => {
        if (msg.textContent.includes('✓') || msg.classList.contains('text-danger')) {
            msg.remove();
        }
    });
}

// ============================================================================
// MÁSCARA AUTOMÁTICA DE CPF
// ============================================================================

const cpfMask = document.querySelector('input[name="cpf"]');
if (cpfMask) {
    cpfMask.addEventListener('input', function() {
        let value = this.value.replace(/\D/g, '');
        
        if (value.length > 11) {
            value = value.slice(0, 11);
        }
        
        if (value.length <= 3) {
            this.value = value;
        } else if (value.length <= 6) {
            this.value = `${value.slice(0, 3)}.${value.slice(3)}`;
        } else if (value.length <= 9) {
            this.value = `${value.slice(0, 3)}.${value.slice(3, 6)}.${value.slice(6)}`;
        } else {
            this.value = `${value.slice(0, 3)}.${value.slice(3, 6)}.${value.slice(6, 9)}-${value.slice(9)}`;
        }
    });
}
