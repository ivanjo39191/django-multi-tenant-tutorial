# core/middleware.py 

import os
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

class TranslationsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        from django.utils import translation
        from django.utils.translation import trans_real, get_language
        from django.conf import settings
        import gettext
        if settings.USE_I18N:
            try:
                # Reset gettext.GNUTranslation cache.
                gettext._translations = {}

                # Reset Django by-language translation cache.
                trans_real._translations = {}

                # Delete Django current language translation cache.
                trans_real._default = None

                settings.LOCALE_PATHS = (os.path.join(settings.BASE_DIR, f'tenant_locale/{connection.schema_name}'), )
                translation.activate(get_language())
            except AttributeError:
                pass