from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class ProductView(View):
 def get(self, request):
  totalitem = 0
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, "totalitem":totalitem})


class ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_carted = False
  if request.user.is_authenticated:
    item_already_carted = Cart.objects.filter(Q(product=product.id) & Q(user = request.user)).exists()
    totalitem = len(Cart.objects.filter(user=request.user))

  return render(request, 'app/productdetail.html', {'product': product, 'item_already_carted':item_already_carted, "totalitem":totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    p_id = request.GET.get('prod_id')
    product = Product.objects.get(id=p_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def showCart(request):
  if request.user.is_authenticated:
    user = request.user
    totalitem = 0

    # provide list of user's cart
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))

    # provide queryset of user's cart
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'app/addtocart.html', {'cart':cart, 'totalamount':totalamount, 'amount':amount,'shipping_amount':shipping_amount,"totalitem":totalitem})
    else: 
      return render(request, 'app/emptycart.html')

@login_required
def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount=70.0
    totalamount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)

@login_required
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount=70.0
    totalamount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)

@login_required
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.delete()
    amount = 0.0
    shipping_amount=70.0
    totalamount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    data = {
      'amount': amount,
      'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)

@login_required
def checkout(request):
  user=request.user
  address = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  totalitem = 0

  shipping_amount = 70.0
  totalamount =0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      totalamount = amount + shipping_amount
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))

  return render(request, 'app/checkout.html', {"address":address, "totalamount":totalamount, "cart_items":cart_items, "totalitem":totalitem})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer  =Customer.objects.get(id = custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    c.delete()
  return redirect("orders")


def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
 add = Customer.objects.filter(user=request.user)
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html', {'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  op =OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html', {"order_placed":op,'totalitem':totalitem})


def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == "Apple" or data == "Samsung":
      mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'below':
      mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt=100000)
    elif data == 'above':
      mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt=100000)

    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})


def laptop(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptops = Product.objects.filter(category = 'L')
    elif data == "DELL" or data == "HP":
      laptops = Product.objects.filter(category = 'L').filter(brand = data)
    elif data == 'below':
      laptops = Product.objects.filter(category = 'L').filter(discounted_price__lt=100000)
    elif data == 'above':
      laptops = Product.objects.filter(category = 'L').filter(discounted_price__gt=100000)

    return render(request, 'app/laptop.html', {'laptops':laptops, 'totalitem':totalitem})



def topwear(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
      topwears = Product.objects.filter(category = 'TW')
    elif data == "Outfitters" or data == "others":
      topwears = Product.objects.filter(category = 'TW').filter(brand = data)
    elif data == 'below':
      topwears = Product.objects.filter(category = 'TW').filter(discounted_price__lt=1000)
    elif data == 'above':
      topwears = Product.objects.filter(category = 'TW').filter(discounted_price__gt=1000)

    return render(request, 'app/topwear.html', {'topwears':topwears, 'totalitem':totalitem})



def bottomwear(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
      bottomwears = Product.objects.filter(category = 'BW')
    elif data == "Denim" or data == "Alzoro":
      bottomwears = Product.objects.filter(category = 'BW').filter(brand = data)
    elif data == 'below':
      bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__lt=1000)
    elif data == 'above':
      bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__gt=1000)

    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears, 'totalitem':totalitem})


# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
  def get(self, request):
    form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form':form})

  def post(self, request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request, 'User Regstered Successfully!')
      form.save()
    return render(request, 'app/customerregistration.html', {'form':form})
    


# def profile(request):
# #  return render(request, 'app/profile.html')
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/profile.html', {'form':form, 
    'active':'btn-primary',  'totalitem':totalitem})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      user=request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']

      reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
      reg.save()
      messages.success(request, "Congratulation, Profile Updated Successfully")
    return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

