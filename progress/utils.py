import importlib

def import_datetieme_format(language_code):
    """uses dinamic importation for get
        the format the in the current lenguage"""
    
    module_prefix =  "django.conf.locale"
    # Construir el nombre del módulo basado en el idioma
    format_name = f"{module_prefix}.{language_code}.formats"

    try:
        # Intentar importar el módulo específico para el idioma
        format = importlib.import_module(format_name)
        return format.DATETIME_FORMAT
    except ImportError:
        # Si el módulo específico para el idioma no existe, importar el módulo predeterminado
        default_format_name = 'django.conf.locale.en.formats.DATETIME_FORMAT'
        default_module = importlib.import_module(default_format_name)
        return default_module.DATETIME_FORMAT