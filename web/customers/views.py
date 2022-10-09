
import os
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic.edit import FormView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.urls import reverse

from django_tenants.management.commands.clone_tenant import Command


from customers.models import Client
from random import choice

from customers.forms import CustomersForm

@method_decorator(never_cache, name='dispatch')
class CustomersFormView(LoginRequiredMixin, FormView):
    login_url = '/admin/login/'
    template_name = 'customers/customers_form.html'
    form_class = CustomersForm

    def get_context_data(self, **kwargs):
        context = super(CustomersFormView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        now_schema_name = connection.schema_name
        name = form.cleaned_data['name']
        from_schema_name = form.cleaned_data['from_schema_name']
        to_schema_name = form.cleaned_data['to_schema_name']
        domain = form.cleaned_data['domain']
        description = form.cleaned_data['description']

        c = Command()
        tenant_data = {'schema_name': to_schema_name, 'name': name, 'description': description}
        tenant = c.store_tenant(clone_schema_from=from_schema_name,
                                    clone_tenant_fields=True,
                                    **tenant_data)
        tenant.name = name
        tenant.save()
        domain_data = {'domain': domain, 'tenant': tenant, 'is_primary': 'True'}
        domain = c.store_tenant_domain(**domain_data)
        connection.set_schema(now_schema_name)
        # locale dir
        from_locale_path = locale_path = os.path.join(settings.BASE_DIR, f'tenant_locale/{from_schema_name}')
        to_locale_path = locale_path = os.path.join(settings.BASE_DIR, f'tenant_locale/{to_schema_name}')
        if not os.path.isdir(to_locale_path):
            print(f"cp -pr {from_locale_path} {to_locale_path}")
            os.system(f"cp -pr {from_locale_path} {to_locale_path}")
        return HttpResponseRedirect(reverse('admin:customers_client_changelist'))

    def get_success_url(self):
        return reverse('admin:customers_client_changelist')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            context = self.get_context_data(**kwargs)
            request.current_app = 'admin'
            context.update(admin.site.each_context(request))
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        # 限制特定使用者才可進入該頁面
        if not request.user.username.startswith('admin') and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))
        context = self.get_context_data(**kwargs)
        request.current_app = 'admin'
        context.update(admin.site.each_context(request))
        return self.render_to_response(context)