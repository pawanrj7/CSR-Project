from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

def index(request):
    return render(request,'user_accounts/index.html')

def email_verify(request):
    return render(request,'user_accounts/email_verify.html')
@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            return redirect('email_verify')
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'user_accounts/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        x = User.objects.get(username=username)
        y = UserProfile.objects.get(user=x)
        print(y.address)
        h=y.address


        user = authenticate(username=username, password=password,)

        if user:
            if user.is_active :
                if  y.category=='Individual':
                    login(request,user)
                else:
                    return HttpResponse("not valid.")

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'user_accounts/login.html')

# Create your views here.

def comp_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        x = User.objects.get(username=username)
        y = UserProfile.objects.get(user=x)
        h=y.address


        user = authenticate(username=username, password=password,)

        if user:
            if user.is_active :
                if  y.category=='Company':
                    login(request,user)
                else:
                    return HttpResponse("not valid.")

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'user_accounts/complogin.html')


def user_profile(request, template_name='user_accounts/user_profile.html'):
    people = UserProfile.objects.all()
    data = {}
    data['people_list'] = people
    return render(request, template_name, data)


def profile_update(request, pk, template_name='user_accounts/profile_update.html'):
    profile = get_object_or_404(UserProfile, pk= pk)
    form = UserProfileInfoForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('user_profile')
    return render(request, template_name, {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account')
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')    