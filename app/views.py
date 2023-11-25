from imaplib import _Authenticator
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404

from operator import ilshift
import os
from unicodedata import category

from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.urls import reverse_lazy

from django.contrib.auth import logout, authenticate, login
from django.core.files.storage import FileSystemStorage
from account.models import Account

from .forms import *
import email
import math
import base64
import requests
import random
import simplejson as json


from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404


import re



content = {}


def sized_render(request, file_name, content):
    
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return render(request, f'mobile/{file_name}', content)
    else:
        return render(request, file_name, content)

def index_page(request):
    content = {}

    
    return render(request, 'index.html', content)
        
# user sector
def personalAccount_page(request):
    return render(request, "personalAccount.html")

def personalAccountTemplates_page(request, name):
    path = f"personalAccountTemplates/template{name}.html"   
    return render(request, path) 

def edit_profile(request):
    try:
        email = request.user
        person = Account.objects.get(email=email)
        if request.method == "POST":
            if request.FILES:
                file = request.FILES['profile_photo']
                filename = f"profile_{str(person.email)}"
                logoImageData = upload_image(file, filename)
                person.userImage = logoImageData[0]
                # shop.prevLogoImage = logoImageData[-1]
            if request.POST.get('first_name', None):
                person.first_name = request.POST['first_name']
            if request.POST.get('last_name', None):
                person.last_name = request.POST['last_name']
            if request.POST.get('phone', None):
                person.phone = request.POST['phone']
            if request.POST.get('city', None):
                person.city = request.POST['city']
            person.save()
            return HttpResponseRedirect("/edit/")
        else:
            content['user'] = person
            return render(request, "editProfile.html", content)
    except Account.DoesNotExist as e:
        raise Http404 from e


# enterance sector
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def login_page(request):
    form = SignUpForm(request.POST)
    content = {
        'form': form
    }
    # enterance request
    if request.method == 'POST' and 'btnform2' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        elif request.POST.get('password') != '':
            print('Try again! username or password is incorrect')
            content['errors'] = 'Try again! username or password is incorrect'
    # registration request
    elif request.method == 'POST' and 'btnform1' in request.POST:
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            username = email
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password, first_name=first_name)
            return redirect('/login/')
        else:
            print(form.errors)

    return sized_render(request, 'signin.html', content)



def forgot_password_page(request):
    return render(request, 'forgotPassword.html')



def service_page(request):

    content = {}

    user = Account.objects.get(id=request.user.id)

    if request.method == 'POST' and 'AddRoom' in request.POST:
        print(request.POST)

        room = Room(
        name = request.POST['name'],
        amount_of_users = int(request.POST['amount_of_users']),
        song = "Shape of my heart",
        timer = 128,
        )
        room.save()

        return redirect('/service/')

    



    # shop = Shop.objects.get(creator=request.user.id)
    # # profile editing
    # if request.method == 'POST' and "profile_saver1" in request.POST:  
    #     user.name_small = request.POST['name_small']
    #     user.nameFull = request.POST['nameFull']
    #     user.ogrn = request.POST['ogrn']
    #     user.inn = request.POST['inn']
    #     user.kpp = request.POST['kpp']
    #     user.street = request.POST['street']
    #     user.fiz_adress = request.POST['fiz_adress']
    #     user.city = request.POST['city']
    #     user.index = request.POST['index']
    #     user.payment_account = request.POST['payment_account']
    #     user.reg_form = request.POST['reg_form']
    #     user.bik = request.POST['bik']
    #     user.korr_check = request.POST['korr_check']
    #     user.save()
    #     return HttpResponseRedirect("/becomeCreator/")
    # # profile editing
    # if request.method == 'POST' and "profile_saver2" in request.POST: 
    #     shop.name = request.POST['name']
    #     shop.description = request.POST['description']
    #     shop.status = request.POST['status']
    #     shop.category = request.POST['chosenCategoties']
    #     if request.FILES:
    #         try:
    #             if request.FILES['logoImage']:
    #                 file = request.FILES['logoImage']
    #                 filename = f"prof_{str(shop.email)}"
    #                 logoImageData = upload_image(file, filename)
    #                 shop.logoImage = logoImageData[0]
    #         except:
    #             pass
    #         try:
    #             if request.FILES['bgImage']:
    #                 file = request.FILES['bgImage']
    #                 filename = f"bg_{str(shop.email)}"
    #                 logoImageData = upload_image(file, filename)
    #                 shop.bgImage = logoImageData[0]
    #         except:
    #             pass
    #     shop.save()
    #     return HttpResponseRedirect("/becomeCreator/")
    # # creating product
    # if request.method == 'POST' and "product_creator" in request.POST:  

    #     # product = Shop_products.objects.get(id = 1)


    #     arr = ['', '' ,'']

    #     # saving image of product
    #     if request.FILES:
    #         file1 = request.FILES['product_photo1']
    #         file2 = request.FILES['product_photo2']
    #         file3 = request.FILES['product_photo3']

    #         filename1 = f'product_photo1_{str(request.user.email)}'
    #         filename2 = f'product_photo2_{str(request.user.email)}'
    #         filename3 = f'product_photo3_{str(request.user.email)}'

    #         logoImageData1 = upload_image(file1, filename1)
    #         logoImageData2 = upload_image(file2, filename2)
    #         logoImageData3 = upload_image(file3, filename3)
    
    #         # picture1 = logoImageData1[0]
    #         # picture2 = logoImageData2[0]
    #         # picture3 = logoImageData3[0]
    #         arr[0] = logoImageData1[0]
    #         arr[1] = logoImageData2[0]
    #         arr[2] = logoImageData3[0]
    #         print(arr)

    #     picture1 = arr[0]
    #     picture2 = arr[1]
    #     picture3 = arr[2]

    #     colors = save_item_compound('color', request.POST, [''])
    #     sizes = save_item_compound('size', request.POST, colors)
    #     colors = save_item_compound('color', request.POST, [''])
    #     sizes = save_item_compound('size', request.POST, colors)
    #     compounds = save_item_compound('compName', request.POST, colors)
    #     percents = save_item_compound('compPerc', request.POST, colors)
    #     prices = save_item_price('price', request.POST, colors, sizes)
    #     amounts =  save_item_price('amount', request.POST, colors, sizes)


    #     product = Shop_products(
    #         product_name = request.POST['product_name'],
    #         description = request.POST['description'],
    #         brand = shop,
    #         show_price = 0,
    #         collection = request.POST['collection'],
    #         # season_winter = request.POST['season_winter'],
    #         # season_spring = request.POST['season_spring'],
    #         # season_summer = request.POST['season_summer'],
    #         # season_autumn = request.POST['season_autumn'],
    #         # season_all = request.POST['season_all'],
    #         country = request.POST['country'],
    #         category = request.POST['type-selector'],
    #         duration = request.POST['duration'],
    #         sex = request.POST['sex'],
    #         id_creator = Account.objects.get(id=request.user.id),
    #         picture1 = picture1,
    #         picture2 = picture2,
    #         picture3 = picture3,
    #     )
    #     product.save()
    #     save_product_adds(request, product, colors, sizes, compounds, percents, prices, amounts)
    #     shop.add_product_id(product.id)
    #     return HttpResponseRedirect("/becomeCreator/")
     
    # if request.method == 'GET' and "product_cards" in request.GET:
    #     print("CARDS")
    # if request.method == 'POST' and "promo_creation" in request.POST:
    #     print(request.POST)
    #     if '' in [request.POST['code'].strip(), request.POST['limit'].strip(), request.POST['type'].strip(), request.POST['val'].strip(),]:
    #         return HttpResponseRedirect("/becomeCreator/") #need error alert
    #     if (int(request.POST['type']) == 0 and int(request.POST['val']) > 100) or int(request.POST['val']) < 1 or int(request.POST['limit']) < 1:
    #         return HttpResponseRedirect("/becomeCreator/") #need error alert
    #     promo = Promocode(
    #         prom = request.POST['code'].strip(),
    #         author = shop,
    #         limit = int(request.POST['limit']),
    #         type = int(request.POST['type']),
    #         value = int(request.POST['val']),
    #     ) 
    #     promo.save()
    
    # # delete cards
    # if request.method == 'GET' and "delete" in request.GET:
    #     shop.products_ids.remove(request.GET['delete'])
    #     product = Shop_products.objects.get(id=request.GET['delete'])
    #     product.delete()
    #     shop.save()
    #     return HttpResponseRedirect("/becomeCreator/")
    # # edit cards
    # if request.method == 'GET' and "edit" in request.GET:
    #     product = Shop_products.objects.get(product_id=request.GET['edit'])
    #     print(product.product_name)
    #     return HttpResponseRedirect("/becomeCreator/")
    # # change status of card
    # if request.method == 'POST' and set(["change_status_to_0", "change_status_to_1", "change_status_to_2", "change_status_to_3"]).intersection(request.POST):
    #     stat = str(set(["change_status_to_0", "change_status_to_1", "change_status_to_2", "change_status_to_3"]).intersection(request.POST))[2:-2]
    #     product = Cart.objects.get(id=request.POST[f'{stat}'])
    #     statuses = {
    #         '0': 'Заказ в обработке',
    #         '1': 'Заказ в процессе сборки',
    #         '2': 'Заказ готов',
    #         '3': 'Заказ в процессе доставки',
    #         '4': 'Заказ доставлен',
    #         '5': 'Заказ отменен',
    #     }
    #     product.status = stat[-1]
    #     product.save()
    #     return HttpResponseRedirect("/becomeCreator/")
    #     # card rejection
    # if request.method == 'POST' and "decline" in request.POST:
    #     product = Cart.objects.get(id=request.POST['decline'])
    #     product.delete()
    #     return HttpResponseRedirect("/becomeCreator/")
    # # create/edit partner
    # if request.method == "POST" and "partner" in request.POST:
    #     try:
    #         partner = Partner.objects.get(email=request.user)
    #         partner.inn = request.POST['INN']
    #         partner.name_small = request.POST['short_name']
    #         partner.payment_account = request.POST['payment_account']
    #         partner.reg_form = request.POST['reg_form']
    #         partner.first_name = request.POST['my_first_name']
    #         partner.last_name = request.POST['my_last_name']
    #         partner.email = user.email
    #         partner.save()
    #     except:
    #         partner = Partner()
    #         partner.inn = request.POST['INN']
    #         partner.name_small = request.POST['short_name']
    #         partner.payment_account = request.POST['payment_account']
    #         partner.reg_form = request.POST['reg_form']
    #         partner.first_name = request.POST['my_first_name']
    #         partner.last_name = request.POST['my_last_name']
    #         partner.email = user.email
    #         partner.save()
    return sized_render(request, 'service.html', content)


def serviceTemplate_page(request, name):
    try :
        content['rooms'] = Room.objects.all()

    except:
        pass
    # try:
    #     user = Account.objects.get(email=request.user.email)
    #     shop = Shop.objects.get(email=request.user)
    #     products = Shop_products.objects.filter(id_creator=account.id)
    #     content['first_name'] = creator.first_name
    #     content['email'] = creator.email
    #     content['creator_avatar'] = creator.cover
    # except:
    #     shop, products = [],[]
    #     content['first_name'] = user.first_name
    #     content['email'] = user.email
    #     content['creator_avatar'] = user.userImage
    path = f"serviceTemplates/template{name}.html"

    # if name == '1':
    #     try:
    #         partner = BePartner.objects.get(email=request.user)
    #         content['partner'] = partner
    #     except:
    #         partner = BePartner()
    #         content['partner'] = partner

    # elif name == '2':
    #     try:
    #         creator = Account.objects.get(email=request.user)
    #         content['creator'] = creator
    #     except:
    #         creator.save()

    # elif name == '3':
    #     try:
    #         categorys = shop.category
    #     except:
    #         categorys = ''
    #     content['shop'] = shop
    #     content['categorys_saver'] = categorys
    #     content['categorys'] = categorys.strip().split(' ') if categorys.strip().split(' ') != [""] else ""

    # elif name == '4':
    #     content['orders'] = [{'info':product} for product in products]
    #     print(content['orders'])
        
    # elif name == '5':
    #     content['products'] = [product for product in products]

    # elif name == '6':
    #     content['promos'] = [promo for promo in Promocode.objects.filter(author = user.id)]

    # elif name == '7':
    #     content['shop'] = shop

    # elif name == '16':
    #     form = ProductCreateForm()
    #     content['form8'] = form
    #     content['shop'] = shop
    return render(request, path, content)

def roomTemplate_page(request, name):
    content={}
    
    room = Room.objects.get(id=name)
    user = Account.objects.get(id=request.user.id)

    content['room'] = room

    if request.method == 'POST' and 'AddToRoom' in request.POST:

        user.room = name
        user.save()

        return redirect('/service/room/'+name+'/')

    if request.method == 'POST' and 'LeaveToRoom' in request.POST:

        user.room = 0
        user.save()

        return redirect('/service/room/'+name+'/')





    return render(request, 'room.html', content)




def partners_page(request):

    # partner = BePartner.objects.all()

    # if request.method == "POST":
    #     user = BePartner.objects.create(
    #         brand_name = request.POST['brand_name'],
    #         name = request.POST['name'],
    #         phone = request.POST['phone'],
    #         city = request.POST['city'],
    #         link = request.POST['link'],
    #         email = request.user.email,
    #         creator = Account.objects.get(id = request.user.id),
    #     )
        
    #     user.save()
    #     return HttpResponseRedirect('/')
    return render(request, 'showPartner.html')
    # else:
    #     return HttpResponseRedirect('/')





