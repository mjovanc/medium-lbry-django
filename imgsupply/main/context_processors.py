from django.conf import settings


def site_title(request):
    return {'SITE_TITLE': settings.SITE_TITLE}
