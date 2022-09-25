from django.views.generic import TemplateView, ListView, DetailView
from products.models import Product

class HomeView(TemplateView):
    template_name = "products/home.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = self.get_context_data(**kwargs)
        context['items'] = products
        return self.render_to_response(context)


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'items'
    paginate_by = 10


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'item'