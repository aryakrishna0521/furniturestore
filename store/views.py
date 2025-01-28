from django.shortcuts import render,redirect
from store.forms import SignUpForm,LoginForm,OrderForm
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from store.models import Furniture,User,BasketItem,Order,OrderItem

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django import views
from django.utils.decorators import method_decorator
from decouple import config

RZP_KEY_ID=config('RZP_KEY_ID')
RZP_KEY_SECRET=config('RZP_KEY_SECRET')

def send_otp_email(user):

    user.generate_otp()
    subject="verify your email"
    message=(f"otp for account verification is{user.otp}")
    from_email="aryakrishna0521@gmail.com"
    to_email=[user.email]
    send_mail(subject,message,from_email,to_email)

# Create your views here.
class SignUpView(views.View):
    template_name="register.html"
    form_class=SignUpForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data)
        if form_instance.is_valid():
            user_object=form_instance.save(commit=False)
            user_object.is_active=False
            user_object.save()
            send_otp_email(user_object)
            return redirect("verify-email")
        return render(request,self.template_name,{"form":form_instance})


 
class VerifyEmailView(views.View):
    template_name="verifyemail.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    def post(self,request,*args,**kwargs):
         otp=request.POST.get("otp")
        #  try:
         user_object=User.objects.get(otp=otp)    
         user_object.is_active=True
         user_object.is_verified=True
         user_object.otp=None
         user_object.save()
         return redirect("sign-in")
         

class IndexView(views.View):
    template_name="index.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
        


class SignInView(views.View):
    template_name="login.html"
    form_class=LoginForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data)
        if form_instance.is_valid():       
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                  login(request,user_object)
                  print("session started")
                  return redirect("index")
            print("invalid credentials")

        return render(request,self.template_name,{"form":form_instance})


class SignOutView(views.View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('sign-in')
        

class ProductListView(views.View):
    template_name="products.html"
    def get(self,request,*args,**kwargs):
        qs=Furniture.objects.all()
   
        return render(request,self.template_name,{"data":qs,})


class ProductDetailview(views.View):
    template_name="detail.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Furniture.objects.get(id=id)
        return render(request,self.template_name,{"data":qs})


class AddToCartView(views.View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        quantity=request.POST.get("quantity")
        product_object=Furniture.objects.get(id=id)
        Basket_object=request.user.cart
        BasketItem.objects.create(
            product_object=product_object,
            quantity=quantity,
            Basket_object=Basket_object,

        )
        print("item has been added to the cart")

        return redirect('cart-summary')


class CartSummaryView(views.View):
    template_name="cart_summary.html"
    def get(self,request,*args,**kwargs):
        qs=BasketItem.objects.filter(Basket_object=request.user.cart,is_order_placed=False)
        basket_item_count=qs.count()
        basket_total=sum([bi.item_total for bi in qs])
        # print(basket_total)
        return render(request,self.template_name,{"basket_items":qs,"baskettotal":basket_total,"basketitemcount":basket_item_count})

class BasketItemDeleteview(views.View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        item_delete=BasketItem.objects.get(id=id).delete()
        return redirect('cart-summary')      



import razorpay


class PlaceOrderView(views.View):
    template_name="place_order.html"
    form_class=OrderForm
    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        qs=request.user.cart.cart_item.filter(is_order_placed=False)
        total=sum(bi.item_total for bi in qs)
        return render(request,self.template_name,{"form":form_instance,"items":qs,"total":total})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=self.form_class(form_data)
        if form_instance.is_valid():
            form_instance.instance.customer=request.user
            order_instance=form_instance.save()
            #add order items

            basket_items=request.user.cart.cart_item.filter(is_order_placed=False )

            payment_method=form_instance.cleaned_data.get("payment_method")
            print(payment_method)
            for bi in basket_items:
                OrderItem.objects.create(
                    order_object=order_instance,
                    product_object=bi.product_object,
                    quantity=bi.quantity,
                    price=bi.product_object.price,

                    
                )
                bi.is_order_placed=True
                bi.save()
           
           
            # rzp integration 
            if payment_method=="ONLINE":
                client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))
                total=sum([bi.item_total for bi in basket_items])*100
                data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }
                payment = client.order.create(data=data)
                rzp_order_id=payment.get("id")
                order_instance.rzp_order_id=rzp_order_id
                order_instance.save()

                context={
                    "amount":total,
                    "currency":"INR",
                    "key_id":RZP_KEY_ID,
                    "order_id":rzp_order_id             
                       }
                return render(request,"payment.html",context)


       
              
       


        return redirect("product-list")


class OrderSummaryView(views.View):
    template_name="order_summary.html"
    def get(self,request,*args,**kwargs):
        qs=request.user.orders.all().order_by("-created_date")
        return render(request,self.template_name,{"orders":qs})


@method_decorator([csrf_exempt],name="dispatch")
class PaymentVerificationView(views.View):
    def post(self,request,*args,**kwargs):
        client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))
        try:
           client.utility.verify_payment_signature(request.POST)
           print("payment success")
           ordet_id=request.POST.get("razorpay_order_id")
           order_object=Order.objects.get(rzp_order_id=ordet_id)
           order_object.is_paid=True
           order_object.save()
           login(request,order_object.customer)



        except:
            print("payment failed")

        print(request.POST)
        return redirect("order-summary")