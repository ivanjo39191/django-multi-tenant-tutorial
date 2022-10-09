from django.db import connection
from django.views.generic import TemplateView, ListView, DetailView
from core.models import Setting
from products.models import Product, ProductCategory
from products.documents import ProductDocument

class HomeView(TemplateView):
    template_name = "products/home.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        left_product_categories = ProductCategory.objects.all()[0:2]
        right_product_categories = ProductCategory.objects.all()[2:3]
        right_product_category = right_product_categories.first() if right_product_categories else None
        context = self.get_context_data(**kwargs)
        context['items'] = products
        context['schema_name'] = connection.schema_name
        context['left_product_categories'] = left_product_categories
        context['right_product_category'] = right_product_category
        return self.render_to_response(context)


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        
        self.query_string = request.GET.get('q', '')
        self.object_list = self.get_queryset()
            
        context = self.get_context_data()
        if self.query_string:
            count = self.object_list.count()
            context['query_string'] = self.query_string
            context['count'] = count
        else:
            context['query_string'] = ''
            context['count'] = 0
        return self.render_to_response(context)

    def get_queryset(self):
        results = ProductDocument.search().query("term", **{"_routing": connection.schema_name})
        if self.query_string:
            results = results.query("match", name=self.query_string)
        return results

class ProductDetailView(DetailView):
    
    model = Product
    context_object_name = 'item'
    
    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        setting = Setting.objects.get(id='zh-hant')
        template_name = 'products/detail/template1.html'
        
        if setting.detail_template == "Template-1":
            template_name = "products/detail/template1.html"
        elif setting.detail_template == "Template-2":
            template_name = "products/detail/template2.html"
        return [template_name]
    
