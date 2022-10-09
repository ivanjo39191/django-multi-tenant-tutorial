# customers/models.py

import os
from django.conf import settings
from django.db import models, connection
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

    def delete(self, force_drop=False, *args, **kwargs):
        """
        Deletes this row. Drops the tenant's schema if the attribute
        auto_drop_schema set to True.
        """
        locale_path = locale_path = os.path.join(settings.BASE_DIR, f'tenant_locale/{connection.schema_name}')
        os.system(f"rm -rf {locale_path}")
        self._drop_schema(force_drop)
        super().delete(*args, **kwargs)

class Domain(DomainMixin):
    pass