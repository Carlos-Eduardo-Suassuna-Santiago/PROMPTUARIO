/**
 * Notifications Script
 * Sistema de notificações em tempo real com polling
 */

const NotificationSystem = {
    // Configurações
    config: {
        pollInterval: 30000, // 30 segundos
        maxNotifications: 5,
        soundEnabled: true,
        desktopNotificationsEnabled: true
    },

    // Estado
    state: {
        isPolling: false,
        lastCheckTime: null,
        notifications: [],
        unreadCount: 0
    },

    /**
     * Inicializar sistema de notificações
     */
    init: function() {
        console.log('Inicializando sistema de notificações...');
        
        // Solicitar permissão para notificações desktop
        if (this.config.desktopNotificationsEnabled && 'Notification' in window) {
            if (Notification.permission === 'default') {
                Notification.requestPermission();
            }
        }

        // Iniciar polling
        this.startPolling();

        // Parar polling ao sair da página
        window.addEventListener('beforeunload', () => {
            this.stopPolling();
        });

        // Reativar polling ao voltar para a página
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopPolling();
            } else {
                this.startPolling();
            }
        });
    },

    /**
     * Iniciar polling de notificações
     */
    startPolling: function() {
        if (this.state.isPolling) return;

        console.log('Iniciando polling de notificações...');
        this.state.isPolling = true;
        this.checkNotifications();

        this.pollingInterval = setInterval(() => {
            this.checkNotifications();
        }, this.config.pollInterval);
    },

    /**
     * Parar polling de notificações
     */
    stopPolling: function() {
        if (!this.state.isPolling) return;

        console.log('Parando polling de notificações...');
        this.state.isPolling = false;
        clearInterval(this.pollingInterval);
    },

    /**
     * Verificar notificações do servidor
     */
    checkNotifications: function() {
        const self = this;

        fetch('/api/notifications/check/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Erro ao buscar notificações');
            return response.json();
        })
        .then(data => {
            if (data.notifications && data.notifications.length > 0) {
                data.notifications.forEach(notification => {
                    self.addNotification(notification);
                });
            }
        })
        .catch(error => {
            console.error('Erro ao verificar notificações:', error);
        });
    },

    /**
     * Adicionar notificação
     */
    addNotification: function(notification) {
        // Verificar se já existe
        if (this.state.notifications.some(n => n.id === notification.id)) {
            return;
        }

        // Adicionar à lista
        this.state.notifications.push(notification);
        this.state.unreadCount++;

        // Limitar número de notificações
        if (this.state.notifications.length > this.config.maxNotifications) {
            this.state.notifications.shift();
        }

        // Mostrar notificação
        this.showNotification(notification);

        // Atualizar badge
        this.updateBadge();
    },

    /**
     * Mostrar notificação visual
     */
    showNotification: function(notification) {
        // Toast no navegador
        this.showToastNotification(notification);

        // Notificação desktop
        if (this.config.desktopNotificationsEnabled && 'Notification' in window && Notification.permission === 'granted') {
            this.showDesktopNotification(notification);
        }

        // Som
        if (this.config.soundEnabled) {
            this.playSound(notification.type);
        }
    },

    /**
     * Mostrar toast notification
     */
    showToastNotification: function(notification) {
        const toast = document.createElement('div');
        toast.className = `notification-toast notification-${notification.type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');

        const iconMap = {
            'check_in': 'user-check',
            'appointment': 'calendar-check',
            'message': 'envelope',
            'alert': 'exclamation-circle',
            'info': 'info-circle'
        };

        const icon = iconMap[notification.type] || 'bell';

        toast.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    <i class="fas fa-${icon}"></i>
                </div>
                <div class="notification-body">
                    <div class="notification-title">${this.escapeHtml(notification.title)}</div>
                    <div class="notification-message">${this.escapeHtml(notification.message)}</div>
                    ${notification.timestamp ? `<div class="notification-time">${this.formatTime(notification.timestamp)}</div>` : ''}
                </div>
                <button class="notification-close" aria-label="Fechar">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Adicionar ao container
        const container = this.getNotificationContainer();
        container.appendChild(toast);

        // Event listeners
        toast.querySelector('.notification-close').addEventListener('click', () => {
            this.removeToast(toast);
        });

        // Auto-remover
        setTimeout(() => {
            this.removeToast(toast);
        }, 5000);
    },

    /**
     * Mostrar notificação desktop
     */
    showDesktopNotification: function(notification) {
        try {
            new Notification(notification.title, {
                body: notification.message,
                icon: '/static/images/Logo.png',
                tag: `notification-${notification.id}`,
                requireInteraction: notification.type === 'alert'
            });
        } catch (error) {
            console.error('Erro ao mostrar notificação desktop:', error);
        }
    },

    /**
     * Reproduzir som
     */
    playSound: function(type) {
        try {
            // Usar Web Audio API para criar som
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            const frequencies = {
                'check_in': 800,
                'appointment': 600,
                'message': 400,
                'alert': 1000,
                'info': 700
            };

            const frequency = frequencies[type] || 600;
            const duration = 0.3;

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        } catch (error) {
            console.error('Erro ao reproduzir som:', error);
        }
    },

    /**
     * Obter ou criar container de notificações
     */
    getNotificationContainer: function() {
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'notification-container';
            document.body.appendChild(container);
        }
        return container;
    },

    /**
     * Remover toast
     */
    removeToast: function(toast) {
        toast.classList.add('removing');
        setTimeout(() => {
            toast.remove();
        }, 300);
    },

    /**
     * Atualizar badge de notificações
     */
    updateBadge: function() {
        const badge = document.querySelector('[data-notification-badge]');
        if (badge) {
            badge.textContent = this.state.unreadCount;
            badge.style.display = this.state.unreadCount > 0 ? 'flex' : 'none';
        }
    },

    /**
     * Marcar notificações como lidas
     */
    markAsRead: function() {
        this.state.unreadCount = 0;
        this.updateBadge();

        fetch('/api/notifications/mark-read/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .catch(error => console.error('Erro ao marcar notificações como lidas:', error));
    },

    /**
     * Formatar tempo
     */
    formatTime: function(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;

        if (diff < 60000) {
            return 'Agora';
        } else if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes}m atrás`;
        } else if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours}h atrás`;
        } else {
            return date.toLocaleDateString('pt-BR');
        }
    },

    /**
     * Escapar HTML
     */
    escapeHtml: function(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    },

    /**
     * Obter CSRF Token
     */
    getCsrfToken: function() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
    }
};

// Inicializar ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    NotificationSystem.init();
});
