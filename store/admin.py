from django.contrib import admin

# Register your models here.
from store.models import Category,Furniture,Colour,Type,User

admin.site.register(Category)
admin.site.register(Furniture)
admin.site.register(Colour)
admin.site.register(Type)
admin.site.register(User)