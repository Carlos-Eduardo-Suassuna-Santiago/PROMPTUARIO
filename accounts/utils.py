from .models import AccessLog

def get_client_ip(request):
    """Obtém o endereço IP real do cliente, considerando proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_access(request, action, details=''):
    """
    Função auxiliar para registrar um evento de acesso.
    """
    if request.user.is_authenticated:
        AccessLog.objects.create(
            user=request.user,
            action=action,
            ip_address=get_client_ip(request),
            details=details
        )
