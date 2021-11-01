from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Product, CaUser, ShoppingBasket, ShoppingBasketItems, OrderItems
from .forms import *
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .permissions import admin_required
from django.core import serializers
from rest_framework import viewsets
from .serializers import *
from rest_framework.authtoken.models import Token
import json


class CaUserSignupView(CreateView):
    model = CaUser
    form_class = CASignupForm
    template_name = 'causer_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class AdminSignupView(CreateView):
    model = CaUser
    form_class = AdminSignupForm
    template_name = 'admin_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class UserViewSet(viewsets.ModelViewSet):
    queryset = CaUser.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'registration.html')


def all_product(request):
    all_p = Product.objects.all()
    flag = request.GET.get('format', '')
    if flag == 'json':
        serialized_products = serializers.serialize('json', all_p)
        return HttpResponse(serialized_products, content_type='application/json')
    return render(request, 'all_product.html', {'products': all_p})


def single_product(request, prodid):
    prod = get_object_or_404(Product, pk=prodid)
    return render(request, 'single_product.html', {'product': prod})


@login_required
@admin_required
def myform(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            return render(request, 'single_product.html', {'product': new_product})
    else:
        form = ProductForm()
        return render(request, 'form.html', {'form': form})


from django.contrib.auth.views import LoginView


class Login(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect('/')


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_to_basket(request, prodid):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        shopping_basket = ShoppingBasket(user_id=user).save()
    # TODO: handle product ID gracefully
    # get shopping basket
    product = Product.objects.get(pk=prodid)
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id, product_id=product.id).first()
    if sbi is None:
        sbi = ShoppingBasketItems(basket_id=shopping_basket, product_id=product.id).save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
    if flag == "json":
        return JsonResponse({'status': 'success'}) # HttpResponse({'status':'x'}, content_type='application/json)
    else:
        return render(request, 'single_product.html', {'product': product, 'added': True})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_basket(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()
    if not shopping_basket:
        shopping_basket = ShoppingBasket(user_id=user).save()
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    flag = request.GET.get('format', '')  # url?format=json&name=John   {'format':'json', 'name':'John'}
    if flag == "json":
        basket_array = []
        for basket_item in sbi:
            tmp = {}
            tmp['product'] = basket_item.product.name
            tmp['price'] = float(basket_item.product.price)
            tmp['quantity'] = int(basket_item.quantity) # [{'name':'price': 'quantity': },{}]
            basket_array.append(tmp)
        return HttpResponse(json.dumps({'items': basket_array}), content_type='application/json')
    else:
        return render(request, 'basket.html', {'basket': shopping_basket, 'items': sbi})

@login_required()
def remove_from_basket(request, sbi):
    sb = ShoppingBasketItems.objects.get(pk=sbi).delete()
    return redirect("/basket/")


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def order_form(request):
    user = request.user
    shopping_basket = ShoppingBasket.objects.filter(user_id=request.user).first()

    # if the shopping basket doesn't is empty
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    if sbi.count() == 0:
        return redirect('/')  # notification telling user basket is empty
    sbi = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    if request.method == "POST":
        ordersform = OrderForm(request.POST, instance=user)
        if ordersform.is_valid():
            order = ordersform.save(commit=False)  # commit=false isn't needed because I specified the instance already
            order.save()
            order_items = []
            for basketitem in sbi:
                order_item = OrderItems(id=order, product=basketitem.product, quantity=basketitem.quantity)
                order_items.append(order_item)
            shopping_basket.delete()
            shopping_basket = ShoppingBasket(user_id=user).save()
            return render(request, "ordercomplete.html", {"order": order, "items": order_items})
    else:
        ordersform = OrderForm(request.POST)
        return render(request, "orderform.html", {"form": ordersform, "basket": shopping_basket, "items": sbi})


def contact_us(request):
    return render(request, 'contactus.html')


def test_json(request):
    products = Product.objects.all()
    se = serializers.serialize("json", products)
    return HttpResponse(se, content_type="application/json")
