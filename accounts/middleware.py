from .models import AccessLog
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

def get_client_ip(request):
    """Obtém o endereço IP real do cliente, considerando proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Registra o login do usuário."""
    AccessLog.objects.create(
        user=user,
        action='login',
        ip_address=get_client_ip(request),
        details=f"Usuário {user.username} logou no sistema."
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Registra o logout do usuário."""
    AccessLog.objects.create(
        user=user,
        action='logout',
        ip_address=get_client_ip(request),
        details=f"Usuário {user.username} saiu do sistema."
    )

class AccessLogMiddleware:
    """
    Middleware para capturar o IP do cliente e garantir que os sinais de login/logout
    tenham acesso ao IP.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Não faz nada aqui, o registro é feito pelos signals
        response = self.get_response(request)
        return response
