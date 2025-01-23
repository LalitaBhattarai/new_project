from django.shortcuts import render,redirect
from .models import Momo_form,Category,Momo
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password   
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import logging

logger=logging.getLogger('django')

# Create your views here.

# def index(request):
#     cateid=None
#     cate=None
#     mo=None
#     try:
#         cate=Category.objects.all()
#         c_id=request.GET.get('category')
#         if c_id:
#             mo=Momo.objects.filter(category=c_id)
#         else:
#             mo=Momo.objects.all()
#         if request.method=="POST":
#             data=request.POST
#             name=data['name']
#             email=data['email']
#             phone=data['phone']
#             message=data['message']
#             user=Momo_form(name=name,email=email,phone=phone,message=message)
#             user.full_clean()
#             user.save()
#             subject="testing"
#             message=render_to_string("main/message.html",{
#                 "name":name,"message":message
#             })
#             from_email=settings.EMAIL_HOST_USER
#             recipient_list=[email]
#             em=EmailMessage(subject,message,from_email,recipient_list)
#             em.send(fail_silently=True)
#             messages.success(request,f"hello {name} we will let you know via your email")
#     except Exception as e:
#         logger.error(str(e),exc_info=True)

#     return render(request,"main/index.html",{
#         'cate':cate,
#         'mo':mo,
#         'cateid':c_id,

        
#     })


def index(request):
    cate=None
    mo=None
    cateid=None
    try:
        cate=Category.objects.all()
        c_id=request.GET.get('category')
        if c_id:
            mo=Momo.objects.filter(category=c_id)
        else:
            mo=Momo.objects.all()
        
        try:
            if request.method=="POST":
                data=request.POST
                name=data['name']
                email=data['email']
                phone=data['phone']
                message=data['message']
                user=Momo_form(name=name,email=email,phone=phone,message=message)
                user.full_clean()
                user.save()
                subject="testing"
                message=render_to_string("main/message.html",{
                    "name":name,"message":message
                })
                from_email=settings.EMAIL_HOST_USER
                recipient_list=[email]
                em=EmailMessage(subject,message,from_email,recipient_list)
                em.send(fail_silently=True)
                messages.success(request,f"hello {name} we will let you know via your email")
        except Exception as e:
            messages.error(request,f"{str(e)}")
    except Exception as f:
        logger.error(str(f),exc_info=True)
    return render(request,"main/index.html",{
        'cate':cate,
        'mo':mo,
        'cateid':c_id
    })


@login_required(login_url='log_in')
def about(request):
    return render(request,"main/about.html")

def contact(request):
    return render(request,"main/contact.html")

def menu(request):
    return render(request,"main/menu.html")

def services(request):
    return render(request,"main/services.html")

def terms(request):
    return render(request,"main/terms.html")


def policy(request):
    return render(request,"main/policy.html")

def privacy(request):
    return render(request,"main/privacy.html")

def support(request):
    return render(request,"main/support.html")





# def register(request):
#     if request.method=='POST':
#         fname=request.POST['first_name']
#         lname=request.POST['last_name']
#         username=request.POST['username']
#         email=request.POST['email']
#         password=request.POST['password']
#         password1=request.POST['password1']

#         if password==password1:
#             try:
#                 validate_password(password)
#                 if User.objects.filter(username=username).exists():
#                     messages.error(request,"username already exixts")
#                     return redirect('register')
                
#                 if User.objects.filter(email=email).exists():
#                     messages.error(request,"email already exixts")
#                     return redirect('register')
                
#                 if not re.search(r'[A-Z]',password):
#                     messages.error(request,"enter atleast one uppercase")
#                     return redirect('register')
        
#                 if not re.search(r'\d',password):
#                     messages.error(request,"enter atleast one numeric case")
#                     return redirect("register")
                
#                 if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?\\|`~]', password):
#                     messages.error(request, "Enter at least one special character")
#                     return redirect("register")
                
#                 User.objects.create_user(first_name=fname, last_name=lname, username=username, email=email,password=password)
#                 messages.success(request,"register successful")
#                 return redirect('login')
            
#             except ValidationError as e:
#                 for error in e.messages:
#                     messages.error(request,error)
#                 return redirect("register")
        
#         else:
#             messages.error(request,"password and confirm password didnt match")
#             return redirect('register')
            
#     return render(request,"auth/register.html")
def register(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        errors = [] 

        if password != password1:
            errors.append("Password and confirm password didn't match.")
        try:
            validate_password(password) 
        except ValidationError as e:
            for error in e.messages:
                errors.append(error)
        
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Enter at least one uppercase letter.")
        
        if not re.search(r'\d', password):
            errors.append("Enter at least one numeric digit.")
        
        if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?\\|`~]', password):
            errors.append("Enter at least one special character.")

        if errors:
            # Display all errors at once if there are any
            for error in errors:
                messages.error(request, error)
            return redirect('register')
        
        User.objects.create_user(first_name=fname, last_name=lname, username=username, email=email, password=password)
        messages.success(request, "Registration successful")
        return redirect('log_in')

    return render(request, "auth/register.html")


def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        remember_me=request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'username is not register yet')
            return redirect('log_in')
 
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)         
            if remember_me:
                request.session.set_expiry(120000)
            else:
                request.session.set_expiry(0)

            next=request.POST.get('next',"")
            return redirect(next if next else 'index')
        else:
            messages.error(request,'password invalid')
            return redirect('log_in')
    next=request.GET.get('next',"")
        
    return render(request,"auth/login.html",{'next':next})



def log_out(request):
    logout(request)
    return redirect(log_in) 


@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    return render(request,'auth/change_password.html',{'form':form})