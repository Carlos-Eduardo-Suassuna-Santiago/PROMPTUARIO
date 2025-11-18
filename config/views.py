from django.http import JsonResponse

def healthcheck(request):
    """Verifica o estado do sistema."""
    return JsonResponse({"status": "ok"})
