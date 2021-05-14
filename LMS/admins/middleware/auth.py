from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request, *args, **kwargs):
        returnUrl = request.META['PATH_INFO']
        print(returnUrl)
        if not request.session.get('user'):
           return redirect(f'/login?return_url={returnUrl}')

        response = get_response(request, *args, **kwargs)

        return response

    return middleware