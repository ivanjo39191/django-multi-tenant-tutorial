import base64
import pickle

from django.http import JsonResponse
from django.views.generic import View, TemplateView
from products.models import Product


class CartView(TemplateView):
    template_name = "orders/cart.html"

    def get(self, request, *args, **kwargs):
        cart_str = request.COOKIES.get('cart', '')
        product_dict = {}
        if cart_str:
            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)
            product_dict = cart_dict.copy()
            for product_id in cart_dict:
                if product := Product.objects.filter(id=product_id):
                    product_dict[product_id]["product"] = product.first()
                else:
                    del product_dict[product_id]
        context = self.get_context_data(**kwargs)
        context["product_dict"] = product_dict
        return self.render_to_response(context)


class AddCartView(View):

    def get(self, request, *args, **kwargs):
        print(self.kwargs)
        product_id = self.kwargs.get('product_id', '')
        cart_str = request.COOKIES.get('cart', '')
        if product_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if product_id in cart_dict:
                cart_dict[product_id]['count'] += 1
            else:
                cart_dict[product_id] = {
                    'count': 1,
                }
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response


class DeleteCartView(View):

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id', '')
        cart_str = request.COOKIES.get('cart', '')
        if product_id:
            if cart_str:
                cart_bytes = cart_str.encode()
                cart_bytes = base64.b64decode(cart_bytes)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            if product_id in cart_dict:
                del cart_dict[product_id]
            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
        context = {}
        context["status"] = 200
        response = JsonResponse(context)
        response.set_cookie("cart", cart_str)
        return response