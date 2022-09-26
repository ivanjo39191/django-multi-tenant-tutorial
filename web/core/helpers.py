import os, time

from django.conf import settings
from django.db import connection

def upload_handle(instance, filename):
    schema_dir = settings.MEDIA_ROOT + '/' + connection.schema_name
    if not os.path.exists(schema_dir):
        os.mkdir(schema_dir)
    dir = schema_dir + '/' + instance.__class__.__name__.lower() + '_media'
    if not os.path.exists(dir):
        os.mkdir(dir)
    name = filename.find('.') and '%s' % os.path.basename(filename).split('.', 1)[0] or ''
    ext = filename.find('.') and '.%s' % os.path.basename(filename).split('.', 1)[1] or ''
    return '/'.join(
        [connection.schema_name, instance.__class__.__name__.lower() + \
        '_media', name + str(int(time.time())) + ext]
    )
