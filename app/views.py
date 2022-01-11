from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from . import models
from .models import Profile, Discounts, Package, Requests, Contact
from .forms import ContactForm
from django.db.models import Count, Max, Min, Avg, Q
from itertools import chain
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as Login_process
from django.contrib.auth.models import User




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
@login_required(login_url="/login")
def request(request):
    packages = models.Package.objects.all()
    msg = None
    if request.method == "POST":
        if request.POST["domain"] in models.Requests.objects.all().values_list('domain',flat=True):
            msg = 'دامنه وارد شده قبلاً استفاده شده، لطفاً نام دیگری وارد کنید'
        else:
            req = Requests()
            req.user = request.user
            req.package = get_object_or_404(Package, id=request.POST['package'])
            req.domain = request.POST['domain']
            req.discount = request.POST['discount']
            if request.POST["discount"] in models.Discounts.objects.filter(active=True).values_list('code',flat=True):
                discount = get_object_or_404(Discounts, code=request.POST['discount'])
                package = get_object_or_404(Package, id=request.POST['package'])
                req.final_price = package.price-(package.price*(discount.discount_percentage/100))
            else:
                package = get_object_or_404(Package, id=request.POST['package'])
                req.final_price = package.price
            req.save()
            return redirect(req.get_absolute_url())
            #return render(request, "checkout.html", { "msg":msg })

    return render(request, "request.html", { "packages":packages, "msg":msg })










#------------------------------------------------------------------------------
def login(request):
    msg = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            Login_process(request, user)
            return redirect("/")
        else:
            msg = 'اطلاعات معتبر نیست'

    return render(request, "login.html", { "msg":msg } )








#------------------------------------------------------------------------------
def signup(request):
    msg = None
    if request.method == "POST":

        if request.POST["username"] in models.User.objects.all().values_list('username',flat=True):
            msg = 'نام کاربری تکراریست'
        elif len(request.POST["phone"]) != 11 :
            msg = 'شماره تماس را تصحیح کنید، شماره باید ۱۱ رقم باشد'
        elif request.POST["phone"][0] != '0' :
            msg = 'شماره تماس را تصحیح کنید، شماره باید با ۰ شروع شود'
        elif request.POST["phone"][1] != '9' :
            msg = 'شماره تماس را تصحیح کنید، شماره باید با ۰۹ شروع شود'
        elif len(request.POST["password"]) < 8 :
            msg = 'رمزعبور را تصحیح کنید، رمزعبور باید حداقل ۸ رقم باشد'
        else:
            user = User()
            user.username = request.POST["username"]
            user.set_password(request.POST['password'])
            user.save()
            profile = get_object_or_404(Profile, user=user)
            profile.phone = request.POST["phone"]
            profile.save()
            msg = 'حساب کاربری شما ایجاد شد - <a style="color:#5f4ded;" href="/login">ورود</a>.'

    return render(request, "signup.html", { "msg":msg })










#------------------------------------------------------------------------------
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    user_reqs = models.Requests.objects.filter(user=request.user)
    msg = None
    if request.method == "POST":
        if len(request.POST["phone"]) != 11 :
            msg = 'شماره تماس را تصحیح کنید، شماره باید ۱۱ رقم باشد'
        elif request.POST["phone"][0] != '0' :
            msg = 'شماره تماس را تصحیح کنید، شماره باید با ۰ شروع شود'
        elif request.POST["phone"][1] != '9' :
            msg = 'شماره تماس را تصحیح کنید، شماره باید با ۰۹ شروع شود'
        #elif len(request.POST["password"]) < 8 :
            #msg = 'رمزعبور را تصحیح کنید، رمزعبور باید حداقل ۸ رقم باشد'
        else:
            user=request.user
            #user.username = request.POST["username"]
            #user.set_password(request.POST['password'])
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            user.save()
            profile = get_object_or_404(Profile, user=user)
            profile.phone = request.POST["phone"]
            profile.save()
            msg = 'تغییرات اعمال شد'



    html_template = loader.get_template( 'profile.html' )
    return HttpResponse(html_template.render( { 'profile':profile, 'user_reqs':user_reqs, 'msg':msg }, request) )











#------------------------------------------------------------------------------
def checkout(request, id):
    req = get_object_or_404(Requests, id=id)
    #discount = get_object_or_404(Discounts, code=req.discount)
    discounts = models.Discounts.objects.filter(active=True)


    html_template = loader.get_template( 'checkout.html' )
    return HttpResponse(html_template.render( { 'req':req, 'discounts':discounts }, request) )














# End
