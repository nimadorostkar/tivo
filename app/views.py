from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from .models import  Discounts, Package, Requests, Contact
from .forms import ContactForm
from django.db.models import Count, Max, Min, Avg, Q
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.contrib import messages






#------------------------------------------------------------------------------
def index(request):
    context = {}
    return render(request, 'index.html', context)




#------------------------------------------------------------------------------
def search(request):
    areas = models.Area.objects.all()
    if request.method=="POST":
        search_buy_status = request.POST['buy_status']
        search_estate_status = request.POST['estate_status']
        search_area = request.POST['area']
        #
        search_rent = request.POST['rent']
        search_rent_rage = search_rent.split(',')
        #
        search_mortgage = request.POST['mortgage']
        search_mortgage_rage = search_mortgage.split(',')
        #
        search_price = request.POST['price']
        search_price_rage = search_price.split(',')
        #
        search_area_size = request.POST['area_size']
        search_area_size_rage = search_area_size.split(',')


        if search:
            general_match = models.Item.objects.filter( Q(buy_status__icontains=search_buy_status) & Q(area__name__icontains=search_area) & Q(estate_status__icontains=search_estate_status)  )
            partial_match = models.Item.objects.filter( Q(area_size__range=(search_area_size_rage[0],search_area_size_rage[1])) )

            if search_buy_status == 'رهن و اجاره':
                price_match = models.Item.objects.filter( Q(rent__range=(search_rent_rage[0],search_rent_rage[1])) & Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) )
            elif search_buy_status == 'فروش':
                price_match = models.Item.objects.filter( Q(price__range=(search_price_rage[0],search_price_rage[1])) )
            elif search_buy_status == 'رهن کامل':
                price_match = models.Item.objects.filter( Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) )
            elif search_buy_status == 'پیش فروش':
                price_match = models.Item.objects.filter( Q(price__range=(search_price_rage[0],search_price_rage[1])) )
            else:
                price_match = models.Item.objects.filter( Q(rent__range=(search_rent_rage[0],search_rent_rage[1])) & Q(deposit__range=(search_mortgage_rage[0],search_mortgage_rage[1])) & Q(price__range=(search_price_rage[0],search_price_rage[1]))  )

            match = list(chain(general_match & partial_match & price_match ))

            if match:
                return render(request,'search.html', {'sr': match, 'areas':areas })
            else:
                messages.error(request,  '   چیزی یافت نشد ، لطفا مجددا جستجو کنید ' )
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'search.html', {'areas':areas })






#------------------------------------------------------------------------------
@login_required(login_url="/login/")
def profile(request):
    current_user = request.user
    profile = models.Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        current_user.username = request.POST['user']
        current_user.first_name = request.POST['firstname']
        current_user.last_name = request.POST['lastname']
        profile.phone = request.POST['phone']
        current_user.email = request.POST['email']
        profile.additional_information = request.POST['additional_information']
        if (request.FILES): profile.user_photo = request.FILES['photo']
        current_user.save()
        profile.save()
        return HttpResponseRedirect('/profile')

    context = {}
    return render(request, 'accounts/profile.html', context)









#------------------------------------------------------------------------------
def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            obj = Contact()
            obj.name = contact_form.cleaned_data['name']
            obj.phone = contact_form.cleaned_data['phone']
            obj.body = contact_form.cleaned_data['body']
            obj.save()
    else:
        contact_form = ContactForm(data=request.POST)

    context = {'contact_form':contact_form}
    context['segment'] = 'contact'
    html_template = loader.get_template( 'contact.html' )
    return HttpResponse(html_template.render(context, request))








#------------------------------------------------------------------------------
def about(request):
    html_template = loader.get_template( 'about.html' )
    return HttpResponse(html_template.render({}, request))






#------------------------------------------------------------------------------
def request(request):
    html_template = loader.get_template( 'request.html' )
    return HttpResponse(html_template.render({}, request))















# End
