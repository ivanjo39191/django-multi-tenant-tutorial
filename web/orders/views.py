import base64
import pickle

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, RelationalProduct
from orders.models import Order
from orders.forms import OrderForm

from orders import ecpay_payment_sdk
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    "orders/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

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


class CheckoutView(FormView):
    template_name = "orders/checkout.html"

    form_class = OrderForm
    success_url = 'orders/confirmation.html'

    def get_cart_cookie(self, request):
        cart_str = request.COOKIES.get('cart', '')
        product_dict = {}
        if cart_str:
            cart_bytes = cart_str.encode()
            cart_bytes = base64.b64decode(cart_bytes)
            cart_dict = pickle.loads(cart_bytes)
        return cart_dict
    
    def get(self, request, *args, **kwargs):
        cart_dict = self.get_cart_cookie(request)
        if cart_dict:
            product_dict = cart_dict.copy()
            total = 0
            for product_id in cart_dict:
                if product := Product.objects.filter(id=product_id):
                    product_dict[product_id]["product"] = product.first()
                    total += int(product_dict[product_id]["count"]) * int(product.first().price)
                else:
                    del product_dict[product_id]
        context = self.get_context_data(**kwargs)
        context["product_dict"] = product_dict
        context["total"] = total
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        cart_dict = self.get_cart_cookie(self.request)
        self.object.save()
        if cart_dict:
            total = 0
            for product_id in cart_dict:
                if product := Product.objects.filter(id=product_id):
                    RelationalProduct.objects.create(order=self.object, product=product.first(), number=cart_dict[product_id]["count"])
                    total += int(cart_dict[product_id]["count"]) * int(product.first().price)
        self.object.total = total
        self.object.save()
        context = self.get_context_data(form=form)
        context['order_id'] = self.object.order_id
        return render(self.request, self.success_url, context=context)


class ECPayView(TemplateView):
    template_name = "orders/ecpay.html"

    def post(self, request, *args, **kwargs):
        scheme = request.is_secure() and "https" or "http"
        domain = request.META['HTTP_HOST']

        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)
        product_list = "#".join([product.name for product in order.product.all()])
        order_params = {
            'MerchantTradeNo': order.order_id,
            'StoreID': '',
            'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'PaymentType': 'aio',
            'TotalAmount': order.total,
            'TradeDesc': order.order_id,
            'ItemName': product_list,
            'ReturnURL': f'{scheme}://{domain}/orders/return/', # ReturnURL為付款結果通知回傳網址，為特店server或主機的URL，用來接收綠界後端回傳的付款結果通知。
            'ChoosePayment': 'ALL',
            'ClientBackURL': f'{scheme}://{domain}/products/list/', # 消費者點選此按鈕後，會將頁面導回到此設定的網址(返回商店按鈕)
            'ItemURL': f'{scheme}://{domain}/products/list/', # 商品銷售網址
            'Remark': '交易備註',
            'ChooseSubPayment': '',
            'OrderResultURL': f'{scheme}://{domain}/orders/orderresult/', # 消費者付款完成後，綠界會將付款結果參數以POST方式回傳到到該網址
            'NeedExtraPaidInfo': 'Y',
            'DeviceSource': '',
            'IgnorePayment': '',
            'PlatformID': '',
            'InvoiceMark': 'N',
            'CustomField1': '',
            'CustomField2': '',
            'CustomField3': '',
            'CustomField4': '',
            'EncryptType': 1,
        }
        # 建立實體
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID='2000132',
            HashKey='5294y06JbISpM5x9',
            HashIV='v77hoKGq4kWxNNIS'
        )
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        ecpay_form = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        context = self.get_context_data(**kwargs)
        context['ecpay_form'] = ecpay_form
        return self.render_to_response(context)



class ReturnView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ReturnView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID='2000132',
            HashKey='5294y06JbISpM5x9',
            HashIV='v77hoKGq4kWxNNIS'
        )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value:
            return HttpResponse('1|OK')
        return HttpResponse('0|Fail')

class OrderResultView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderResultView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):

        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID='2000132',
            HashKey='5294y06JbISpM5x9',
            HashIV='v77hoKGq4kWxNNIS'
        )
        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        order_id = request.POST.get('MerchantTradeNo')
        rtnmsg = request.POST.get('RtnMsg')
        rtncode = request.POST.get('RtnCode')
        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value and rtnmsg == 'Succeeded' and rtncode == '1':
            order = Order.objects.get(order_id=order_id)
            order.status = 'waiting_for_shipment'
            order.save()
            return HttpResponseRedirect('/orders/order_success/')
        return HttpResponseRedirect('/orders/order_fail/')

class OrderSuccessView(TemplateView):
    template_name = "orders/order_success.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
class OrderFailView(TemplateView):
    template_name = "orders/order_fail.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)