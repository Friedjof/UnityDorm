def version_context_processor(request):
    from django.conf import settings
    return {
        'VERSION': settings.VERSION,  # Die Versionsnummer aus settings.py
    }

def year_context_processor(request):
    import datetime
    return {
        'YEAR': datetime.datetime.now().year,  # Das aktuelle Jahr
    }
