
def cookie_token_middleware(get_response):

    def middleware(request):
        # Set Authorization header if Token cookie is present.
        if request.COOKIES.get('Token') is not None:
            request.META['HTTP_AUTHORIZATION'] = 'Token ' + \
                request.COOKIES['Token']

        return get_response(request)

    return middleware
