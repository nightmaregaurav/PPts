from django.conf import settings

from ..models import SiteSetting


site_settings_abstract = {
    'site_logo': r'#',
    'site_title': r'PUBG points table generator (PPts)',
    'header_main': r'PUBG <span style="font-family: sans-serif;">Points Tables</span>',
    'footer_main': r'<span><span style="font-family: sans-serif;">&copy;Copyright reserved ~ Gaurav Nyaupane |</span> '
                   r'PUBG <span style="font-family: sans-serif;">Points Tables</span></span> '
}


def urls(request):
    app = request.resolver_match.app_name
    if app:
        app += '/'

    app = app.strip()

    return {
        'APP_URL': app,
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'BASE_URL': 'base.html',
    }


# noinspection PyUnusedLocal
def site_setting(request):
    site_settings = SiteSetting.objects.all()
    for setting in site_settings:
        site_settings_abstract[setting.key] = setting.value
    return {
        'site_setting': site_settings_abstract,
    }
