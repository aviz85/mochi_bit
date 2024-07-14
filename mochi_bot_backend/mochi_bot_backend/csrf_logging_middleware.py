import logging
from django.middleware.csrf import CsrfViewMiddleware, get_token

logger = logging.getLogger(__name__)

class CsrfLoggingMiddleware(CsrfViewMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        response = super().process_view(request, callback, callback_args, callback_kwargs)
        if response is None:
            csrf_token = get_token(request)
            logger.debug(f'CSRF token: {csrf_token}')
        return response

    def process_exception(self, request, exception):
        if hasattr(exception, 'csrf_token'):
            logger.error(f'CSRF verification failed: {exception}')
        return None