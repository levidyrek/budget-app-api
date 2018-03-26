from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


class TokenCookieAuthentication(TokenAuthentication):
    """
    Custom token authentication. Checks for a token in a cookie after
    checking the Authorization header.
    """

    def authenticate(self, request):
        header_result = \
            super(TokenCookieAuthentication, self).authenticate(request)

        # If Authorization header is not populated, check cookies.
        if header_result is None:
            try:
                token = request.get_signed_cookie(self.keyword, default=None)
                if token is not None:
                    return self.authenticate_credentials(token)
            except Exception as e:
                raise exceptions.AuthenticationFailed(str(e))

        return header_result
