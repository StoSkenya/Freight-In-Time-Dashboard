from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, \
 PermissionRequiredMixin

from django.shortcuts import get_object_or_404
 
from django.views.generic import ListView, DetailView 
from django.urls import reverse_lazy

from .forms import CreateQuoteLogForm
from .models import QuoteLogdb
from .analyics import Locodes,Management

import json
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='login')
def quotelog_create(request):
    """
        # Create QuoeLogs from form

    """

    context = {}

    form = CreateQuoteLogForm(request.POST or None)
    # # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()
        messages.success(request, 'Form submission successful')
        # redirect to another page with success message
        # return HttpResponse('Success')
        return redirect('logs:view_ql')
    # return HttpResponseRedirect(request.path_info)
    # redirect to detail view
    
         
    context['form'] = form

    context['ls'] = ['ke', 'ug']

    return render(request, "quotelogs/create.html", context)


@login_required(login_url='login')
def update_quotelogs(request,id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(QuoteLogdb, id = id)
 
    # pass the object as instance in form
    form = CreateQuoteLogForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.success(request, 'QuoteLog update successful')
        return redirect('logs:view_ql')
        # return reverse_lazy('quotelogs:view_quotelogs')
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "quotelogs/update.html", context)

# views
class QuoteLogListView(ListView):
    """
        # View Quotelogs by office
    """ 
    model = QuoteLogdb
    template_name = "quotelogs/view_all.html"

class QLManagement_DetialView(ListView):
    """
        # View all quotelogs by management for every office
    """ 
    model = QuoteLogdb
    template_name = "quotelogs/management_viewall.html"
    
class QuoteLogDetialView(DetailView):
    """
    """ 
    model = QuoteLogdb
    template_name = "quotelogs/detail_view.html"


@login_required(login_url='login')
def sum_win_ratio_by_yrs(request):
    # query
    context = {}
    user = request.user  
    designation = request.user.profile.designation
    
    # Get data from db and append to our analytics class
    quotelogs_mdl = QuoteLogdb.objects.all()[:1000]
    analytics = Management(designation, quotelogs_mdl)

    # get all win ratios by year
    context['Tot_win_ratios'] = zip(analytics.sum_win_ratio_by_yrs()['years'],analytics.sum_win_ratio_by_yrs()['ratios'])
    # print(context)
    # print(analytics.product_wr_by_yrs())
    return render(request, 'analytics/winratios.html',context)


# api
@login_required(login_url='login')
def biztype_winratio_API(request):
    designation = request.user.profile.designation
    
    # Get data from db and append to our analytics class
    quotelogs_mdl = QuoteLogdb.objects.all()[:1000]
    analytics = Management(designation, quotelogs_mdl)
    context = analytics.business_type_wr_by_yrs()
    if request.method == 'GET':
        context = analytics.business_type_wr_by_yrs()
    return HttpResponse(json.dumps(context), content_type="application/json")

# api
# Get counts for all countries
@login_required(login_url='login')
def countsmanagement(request):
    # query
    context = {}
    user = request.user
    designation = request.user.profile.designation
    quotelogs_mdl = QuoteLogdb.objects.all()
    analytics = Management(designation, quotelogs_mdl)

    a,b = analytics.management_count()
    c = analytics.basic_counts()
    
    context['basic_counts_by_office'] = c
    context['freight_mode_counts_by_office'] = a
    context['business_type_counts_by_office'] = b
    # main home page for users
    return HttpResponse(json.dumps(context), content_type="application/json")

# api
# get locodes by country
@login_required(login_url='login')
def get_codes(request, country):
    context = {}
    locades = list(Locodes(country).by_country())
    if request.method == 'GET':
        context['countries'] = locades

    # print(context)
    return HttpResponse(json.dumps(context), content_type="application/json")







