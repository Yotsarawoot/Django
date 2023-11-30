from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from songline import Sendline
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse

# Create your views here.
global_context = {}

def home(request):
    product = productPS5.objects.all()
    product_per_page = 3
    paginator = Paginator(product, product_per_page)
    page = request.GET.get('page')
    product = paginator.get_page(page)

    data = { 'allproduct': product }

    allrow = []
    row = []
    for i,p in enumerate(product):
        if i%3 == 0:
            if i != 0:
                allrow.append(row)
            row = []
            row.append(p)
        else:
            row.append(p)
    allrow.append(row)
    data['allrow'] = allrow

    return render(request, 'myapp/home.html', data)


def home2(request):
    product = productPS4.objects.all()
    product_per_page = 3
    paginator = Paginator(product, product_per_page)
    page = request.GET.get('page')
    product = paginator.get_page(page)

    data = { 'allproduct': product }

    allrow = []
    row = []
    for i,p in enumerate(product):
        if i%3 == 0:
            if i != 0:
                allrow.append(row)
            row = []
            row.append(p)
        else:
            row.append(p)
    allrow.append(row)
    data['allrow'] = allrow

    return render(request, 'myapp/home2.html', data)


def home3(request):
    product = productNintendo.objects.all()
    product_per_page = 3
    paginator = Paginator(product, product_per_page)
    page = request.GET.get('page')
    product = paginator.get_page(page)

    data = { 'allproduct': product }

    allrow = []
    row = []
    for i,p in enumerate(product):
        if i%3 == 0:
            if i != 0:
                allrow.append(row)
            row = []
            row.append(p)
        else:
            row.append(p)
    allrow.append(row)
    data['allrow'] = allrow

    return render(request, 'myapp/home3.html', data)


def aboutUs(request):
    return render(request, 'myapp/aboutus.html')


def contact(request):

    token = 'wVOWD9B58zd3yHMakWzNLB23YmRPED03rxCh8ZzaN2h'
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        topic = data.get('topic')
        email = data.get('email')
        detail = data.get('detail')

        if (topic == '' or email == '' or detail == ''):
            context['message'] = 'Please, fill in all contact informations'
            return render(request, 'myapp/contact.html', context)

        newRecord = contactList()
        newRecord.topic = topic
        newRecord.email = email
        newRecord.detail = detail
        newRecord.save()

        context['message'] = 'The message has been received'

        m = Sendline(token)
        m.sendtext('\ntopic:{0}\nemail:{1}\ndetail:{2}'.format(topic, email, detail))

    return render(request, 'myapp/contact.html', context)


def addInfo(request):

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        type = data.get('type')
        title = data.get('title')
        descript = data.get('descript')
        price = data.get('price')
        stock = data.get('stock')

        print(title)
        print(descript)
        print(price)
        print(stock)
        print('File', request.FILES)

        if (type == '' or title == '' or descript == ''or price == ''or stock == ''):
            context['message'] = 'Please, fill in all informations'
            return render(request, 'myapp/contact.html', context)
        
        if (type == 'PS5'):
            newTitle = productPS5()
        elif (type == 'PS4'):
            newTitle = productPS4()
        elif (type == 'NDS'):
            newTitle = productNintendo()

        newTitle.title = title
        newTitle.description = descript
        newTitle.price = price
        newTitle.stock = stock

        if 'picture' in request.FILES:
            file_image = request.FILES['picture']
            file_image_name = file_image.name.replace(' ', '')
            if (type == 'PS5'):
                fs = FileSystemStorage(location='media/productPS5')
            elif (type == 'PS4'):
                fs = FileSystemStorage(location='media/productPS4')
            elif (type == 'NDS'):
                fs = FileSystemStorage(location='media/productNTD')
            filename = fs.save(file_image_name, file_image)
            upload_file_url = fs.url(filename)
            print('Picture url: ', upload_file_url)
            if (type == 'PS5'):
                newTitle.picture = 'productPS5' + upload_file_url[6:]
            elif (type == 'PS4'):
                newTitle.picture = 'productPS4' + upload_file_url[6:]
            elif (type == 'NDS'):
                newTitle.picture = 'productNDS' + upload_file_url[6:]
            

        if 'specfile' in request.FILES:
            file_specfile = request.FILES['specfile']
            file_specfile_name = file_specfile.name.replace(' ', '')
            if (type == 'PS5'):
                fs = FileSystemStorage(location='media/specfilePS5')
            elif (type == 'PS4'):
                fs = FileSystemStorage(location='media/specfilePS4')
            elif (type == 'NDS'):
                fs = FileSystemStorage(location='media/specfileNDS')
            filename = fs.save(file_specfile_name, file_specfile)
            upload_file_url = fs.url(filename)
            print('Specfile url: ', upload_file_url)
            if (type == 'PS5'):
                newTitle.specfile = 'productPS5' + upload_file_url[6:]
            elif (type == 'PS4'):
                newTitle.specfile = 'productPS4' + upload_file_url[6:]
            elif (type == 'NDS'):
                newTitle.specfile = 'productNDS' + upload_file_url[6:]
            
        newTitle.save()

        context['message'] = 'The message has been received'

    return render(request, 'myapp/addinfo.html')


def userLogin(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')
        password = data.get('password')

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home_page')
        except:
            context['message'] = "username or password is incorrect."
            
    # print("{0}".format(context))
    return render(request, 'myapp/login.html', context)


@permission_required('is_superuser' ,login_url='/login')
def showContact(request):
    allcontact = contactList.objects.all()
    context = {'contact': allcontact}
    return render(request, 'myapp/showcontact.html', context)


def userRegister(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repassword = data.get('repassword')

        try:
            User.objects.get(username=username)
            context['message'] = "Username duplication"
        except:
            newuser = User()
            newuser.username = username
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.email = email

            if (password==repassword):
                newuser.set_password(password)
                newuser.save()
                newprofile = profile()
                newprofile.user = User.objects.get(username=username)
                newprofile.save()
                context['message'] = "register complete."
            else:
                context['message'] = "password or re-password is incorrect."


    return render(request, 'myapp/register.html', context)


def userProfile(request):
    context = {}
    userprofile = profile.objects.get(user=request.user)
    context['profile'] = userprofile
    global_context['profile'] = userprofile
    return render(request, 'myapp/profile.html', context)


def editProfile(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        current_user = User.objects.get(id=request.user.id)
        current_user.first_name = firstname
        current_user.last_name = lastname
        current_user.username = username
        current_user.email = email
        current_user.set_password(password)
        current_user.save()

        try:
            userLogin(request)
            return redirect('home_page')
        except:
            context['message'] = "Edit Profile Fail"
            return render(request, 'myapp/editprofile.html', context)

    return render(request, 'myapp/editprofile.html', global_context)


def actionPage(request, cid):
    
    context = {}
    contact = contactList.objects.get(id=cid)
    context['contact'] = contact
    

    try:
        actions = action.objects.get(contactList=contact)
        context['action'] = actions
    except:
        pass

    if request.method == 'POST':
        data = request.POST.copy()
        actiondetail = data.get('actiondetail')

        if 'save' in data:
            try:
                check = action.objects.get(contactList=contact)
                check.actionDetail = actiondetail
                check.save()
                context['action'] = check
            except:
                new = action()
                new.contactList = contact
                new.actionDetail = actiondetail
                new.save()

        elif 'delete' in data:
            try:
                contact.delete()
                return redirect('showcontact_page')
            except:
                pass

        elif 'complete' in data:
            contact.complete = True
            contact.save()
            return redirect('showcontact_page')
        
    return render(request, 'myapp/action.html', context)


def handler404(request, exception):
    return render(request, 'myapp/404errorPage.html')


def gameDetailPage(request, type, cid):
    context = {}
    if type == 'ps5':
        game = productPS5.objects.get(id=cid)
    elif type == 'ps4':
        game = productPS4.objects.get(id=cid)
    elif type == 'NTD':
        game = productNintendo.objects.get(id=cid)
    context['game'] = game
    print(context['game'])

    return render(request, 'myapp/gamedetail.html', context)


class CrudView(TemplateView):
    template_name = 'myapp/crud.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CrudUser.objects.all()
        return context


class CreateCrudUser(View):
    def  get(self, request):
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.create(
            name = name1,
            address = address1,
            age = age1
        )

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)

class DeleteCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        CrudUser.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.get(id=id1)
        obj.name = name1
        obj.address = address1
        obj.age = age1
        obj.save()

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)