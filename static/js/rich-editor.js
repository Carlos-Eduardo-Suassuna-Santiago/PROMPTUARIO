    /**
 * Rich Text Editor Script
 * Integra Quill.js para edição de texto rico em prontuários
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeRichEditors();
});

/**
 * Inicializar editores de texto rico
 */
function initializeRichEditors() {
    const editorContainers = document.querySelectorAll('[data-editor="rich"]');
    
    editorContainers.forEach((container, index) => {
        const editorId = container.id || `editor-${index}`;
        container.id = editorId;
        
        // Criar editor Quill
        const quill = new Quill(`#${editorId}`, {
            theme: 'snow',
            placeholder: 'Digite o conteúdo do prontuário...',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'color': [] }, { 'background': [] }],
                    ['link'],
                    ['clean']
                ]
            }
        });

        // Sincronizar com campo oculto
        const hiddenField = container.parentNode.querySelector('textarea[name]');
        if (hiddenField) {
            // Carregar conteúdo existente
            if (hiddenField.value) {
                try {
                    const delta = JSON.parse(hiddenField.value);
                    quill.setContents(delta);
                } catch (e) {
                    // Se não for JSON válido, tratar como texto plano
                    quill.setText(hiddenField.value);
                }
            }

            // Atualizar campo oculto ao editar
            quill.on('text-change', function() {
                hiddenField.value = JSON.stringify(quill.getContents());
            });

            // Validação no submit do formulário
            const form = hiddenField.closest('form');
            if (form) {
                form.addEventListener('submit', function(e) {
                    // Verificar se o editor está vazio
                    if (quill.getText().trim().length === 0) {
                        e.preventDefault();
                        showNotification('Por favor, preencha o conteúdo do prontuário.', 'warning');
                        return false;
                    }
                });
            }
        }

        // Armazenar referência global
        window[`quill_${editorId}`] = quill;
    });
}

/**
 * Obter conteúdo do editor
 */
function getEditorContent(editorId) {
    const quill = window[`quill_${editorId}`];
    if (quill) {
        return quill.getContents();
    }
    return null;
}

/**
 * Obter conteúdo em HTML
 */
function getEditorHtml(editorId) {
    const quill = window[`quill_${editorId}`];
    if (quill) {
        const container = quill.container.querySelector('.ql-editor');
        return container.innerHTML;
    }
    return '';
}

/**
 * Obter conteúdo em texto plano
 */
function getEditorText(editorId) {
    const quill = window[`quill_${editorId}`];
    if (quill) {
        return quill.getText();
    }
    return '';
}

/**
 * Definir conteúdo do editor
 */
function setEditorContent(editorId, content) {
    const quill = window[`quill_${editorId}`];
    if (quill) {
        if (typeof content === 'string') {
            try {
                const delta = JSON.parse(content);
                quill.setContents(delta);
            } catch (e) {
                quill.setText(content);
            }
        } else {
            quill.setContents(content);
        }
    }
}

/**
 * Limpar editor
 */
function clearEditor(editorId) {
    const quill = window[`quill_${editorId}`];
    if (quill) {
        quill.setContents([]);
    }
}

/**
 * Desabilitar editor
 */
function disableEditor(editorId) {
    const quill = window[`quill_${editorId}`];
    if (quill) {
        quill.disable();
    }
}

/**
 * Habilitar editor
 */
function enableEditor(editorId) {
    const quill = window[`quill_${editorId}`];
    if (quill) {
        quill.enable();
    }
}

/**
 * Mostrar notificação
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}
