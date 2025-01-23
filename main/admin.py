from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Momo_form)
class Display(admin.ModelAdmin):
    list_display=['name','email','phone','message']
    
 


admin.site.register([Category,Momo])

