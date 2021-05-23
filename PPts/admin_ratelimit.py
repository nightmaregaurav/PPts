from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from ratelimit.decorators import ratelimit


def login_wrapper(login_function):
    @ratelimit(key='ip', method='POST', rate='5/5m')
    def admin_login(request, **kwargs):
        if getattr(request, 'limited', False):
            messages.error(request, "Too many login attempt detected, please try after 5 minutes.")
            return redirect(reverse('admin:index'))
        else:
            return login_function(request, **kwargs)

    return admin_login
