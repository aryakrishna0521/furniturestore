
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from random import randint



class User(AbstractUser):
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,null=True,blank=True)
    def generate_otp(self):
        self.otp=str(randint(1000,9000))
        self.save()


class BaseModel(models.Model):
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

class Category(BaseModel):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Colour(BaseModel):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Type(BaseModel):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Furniture(BaseModel):
    
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=100, null=True)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True)
    price = models.FloatField(null=True)
    picture= models.ImageField(upload_to='images/', null=True)
    color_object=models.ManyToManyField(Colour)
    type_object=models.ForeignKey(Type,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Basket(BaseModel):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')

     

class BasketItem(BaseModel):
    product_object=models.ForeignKey(Furniture,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    Basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name='cart_item')
    is_order_placed=models.BooleanField(default=False)

    @property
    def item_total(self):

         return self.product_object.price*self.quantity

    


class Order(BaseModel):

    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    address=models.TextField()

    phone=models.CharField(max_length=20)

    PAYMENT_OPTIONS=(
        ("COD","COD"),
        ("ONLINE","ONLINE")
    )

    payment_method=models.CharField(max_length=15,choices=PAYMENT_OPTIONS,default="COD")

    rzp_order_id=models.CharField(max_length=100,null=True)

    is_paid=models.BooleanField(default=False)


    def order_total(self):
        total=sum([oi.item_total for oi in self.orderitems.all()])

        return total





class OrderItem(BaseModel):

    order_object=models.ForeignKey(
                                   Order,on_delete=models.CASCADE,
                                   related_name="orderitems"
                                   )
    
    product_object=models.ForeignKey(Furniture,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(default=1)


    price=models.FloatField()

    @property
    def item_total(self):
        return self.price*self.quantity


def create_basket(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)
post_save.connect(create_basket,User)

