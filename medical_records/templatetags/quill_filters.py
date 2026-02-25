import json
from django import template

register = template.Library()


@register.filter
def quill_to_text(value):
    """
    Converte formato Quill Delta JSON para texto legível.
    Ex: {"ops":[{"insert":"Teste\n"}]} → "Teste"
    """
    if not value:
        return "N/A"
    
    try:
        # Se for string JSON, fazer parse
        if isinstance(value, str):
            data = json.loads(value)
        else:
            data = value
        
        # Extrair texto dos ops
        text = ""
        if isinstance(data, dict) and 'ops' in data:
            for op in data.get('ops', []):
                if 'insert' in op:
                    text += op['insert']
        
        # Remover quebras de linha finais e retornar
        return text.strip() if text.strip() else "N/A"
    except (json.JSONDecodeError, TypeError, KeyError):
        return value if value else "N/A"
