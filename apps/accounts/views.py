from django.shortcuts import render, redirect
from django import views
from .forms import UserLoginForm, UserRegisterationForm, VerifyCodeForm
import random
from utils import send_otp_code
from .models import OtpCode ,User
from django.contrib import messages
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

class UserRegisterView(views.View):
    form_class = UserRegisterationForm
    template_name = 'accounts/register.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            old_code = OtpCode.objects.filter(phone_number = cd['phone_number'])
            if old_code:
                old_code[0].delete()
            send_otp_code(phone_number=cd['phone_number'], code= random_code)
            OtpCode.objects.create(phone_number= cd['phone_number'], code = random_code)
            request.session['user_registeration_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password'],
            }
            messages.success(request, 'Code was sent.')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})
    
class UserRegisterVerifyCodeView(views.View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_info = request.session['user_registeration_info']
        form = self.form_class(request.POST)
        code_instance = OtpCode.objects.get(phone_number = user_info['phone_number'])
        if form.is_valid():
            cd  = form.cleaned_data
            if cd['code'] == code_instance.code:
                if code_instance.created + timezone.timedelta(minutes=2) < timezone.now() :
                    messages.error(request, 'Code was expired', 'danger')
                    return redirect('accounts:register')
                else:
                    code_instance.delete()
                    User.objects.create_user(email= user_info['email'], phone_number= user_info['phone_number'], 
                                            full_name= user_info['full_name'], password= user_info['password'])
                    messages.success(request, 'You are registered.', 'success')
                    return redirect('home:home')
            else:
                messages.error(request, 'Wrong code', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
    

class UserLoginView(views.View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            old_code = OtpCode.objects.filter(phone_number = cd['phone_number'])
            if old_code:
                old_code[0].delete()
            send_otp_code(phone_number=cd['phone_number'], code= random_code)
            OtpCode.objects.create(phone_number= cd['phone_number'], code = random_code)
            request.session['user_registeration_info'] = {
                'phone_number': cd['phone_number'],
                'password': cd['password'],
            }
            messages.success(request, 'Code was sent.')
            return redirect('accounts:login_verify_code')
        return render(request, self.template_name, {'form': form})
    
class UserLoginVerifyCodeView(views.View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_info = request.session['user_registeration_info']
        form = self.form_class(request.POST)
        code_instance = OtpCode.objects.get(phone_number = user_info['phone_number'])
        if form.is_valid():
            cd  = form.cleaned_data
            if cd['code'] == code_instance.code:
                if code_instance.created + timezone.timedelta(minutes=2) < timezone.now() :
                    messages.error(request, 'Code was expired', 'danger')
                    return redirect('accounts:register')
                else:
                    code_instance.delete()
                    user = authenticate(phone_number= user_info['phone_number'], password= user_info['password'])
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'You are loged in.', 'success')
                        return redirect('home:home')
                    else:
                        messages.error(request, 'Wrong username or password.', 'danger')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Wrong code', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
    
class UserLogoutView(views.View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are loged out')
        return redirect('home:home')