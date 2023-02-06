from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import FITUser, Profile
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm #add this


from quotelog.models import QuoteLogdb as qdb
from .ql_analytics import QLAnalytics
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import logout

import json
from django.http import HttpResponse
# ------------- views


def signup(request):
    """
        # User signup office email, profile: country, office,designation
    """
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            #  Create the user profile
            Profile.objects.create(user=new_user)
            login(request, new_user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('create_profile')
    else:
        user_form = SignUpForm()
    return render(request, 'accounts/registration/signup.html', {'user_form': user_form})



@login_required(login_url='login')
def get_sum_quotes(request):
    """
        # Get a summation/number of quotes done by current logged in users office
    """
    context = {} 
    ql_mdl = qdb.objects.all()
    # print(ql_mdl)
    analytics_cls = QLAnalytics(request.user.profile.office,ql_mdl)
    # print(f"Office coount: {}")
    
    if request.method == 'GET':
        context['q_id'] = int(analytics_cls.sum_office())
    return HttpResponse(json.dumps(context), content_type="application/json")


def user_login(request):
    """
        #  User login
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                
                if request.user.profile.designation != 'MANAGEMENT':
                    print(request.user.profile.designation)
                    messages.success(request, 'Your profile was updated.')
                    messages.info(request, f"You are now logged in as {email}.")
                    return redirect("home")
                if request.user.profile.designation == 'MANAGEMENT':
                    print(request.user.profile.designation)
                    messages.success(request, 'Your profile was updated.')
                    messages.info(request, f"You are now logged in as {email}.")
                    return redirect('management')

            else:
                messages.error(request, "Invalid username or password.")
    else:
        messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
    return render(request=request, template_name="accounts/registration/login.html", context={"login_form": form})

@login_required(login_url='login')
def create_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(
            instance=request.user.profile, data=request.POST)

        if profile_form.is_valid():
            # current_user = request.user
            profile_form.save()
            return redirect('home')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/registration/profile.html', {'profile_form': profile_form})

@login_required(login_url='login')
def home(request):
    context = {} 
    return render(request, 'home/home.html',context )


@login_required(login_url='login')
def management(request):
    # this will be home page for management

    # get all quotelogs
    context = {}

    # 

    return render(request=request,template_name='home/home_management.html',context=context)


# logout
def logout_view(request):
    logout(request)
    return redirect('login')

