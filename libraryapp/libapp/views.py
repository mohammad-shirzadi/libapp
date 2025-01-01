from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return HttpResponse('salam')




#request={"status" : "login/signup", 'username':'UN', password:'PW', 'fname' : 'fname', 'lname': 'lname', 'email':'email', }
def login(request):
    print(request.POST.get)
    if request.method == 'GET':
        context = {
            'page' : 'login',
            'st' : 'notLogin',
            'msg' : ""
        }
        return render(request,'libapp/login.html',context)
    elif request.POST.get('login'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr = authenticate(request,username=username,password=password)
        if usr:
            request.session['user_id'] = User.objects.get(username=username).id
            
            context = {
                'page': 'login',
                'st' : 'loggedin',
                'msg' : "You're logged in."
            }
            #return HttpResponse("You're logged in.")
            return render(request,'libapp/login.html',context)
        else:
            context = {
                'page' : 'login',
                'st' : 'not login',
                'msg' : "Your Username and Password didn't match."
            }
            #return HttpResponse("Your Username and Password didn't match.")
            return render(request,'libapp/login.html',context)
    return HttpResponse('')
def signup(request):
    if request.method == 'POST':
        ##TODO  use while to ask agin when some field is empty
        Fname = request.POST.get('Fname')
        Lname = request.POST.get('Lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username):
            ##TODO  send Email and verifying email address
            newusr.first_name = Fname
            newusr.last_name = Lname
            newusr = User.objects.create_user(lastnname=Lname,firstname=Fname ,username=username, email=email,password=password)
            newusr.save()
            context = {
                'page' : 'signup',
                'st' : 'notLogin',
                'msg' : "your account is created",
            }
        else: 
            context = {
                'page' : 'signup',
                'st' : 'notLogin',
                'msg' : "your username is not available"
            }

        return render(request,'libapp/signup.html',context)
    else:
        context = {
            'page' : 'signup',
            'st' : 'notLogin',
            'msg' : ""
        }
        return render(request,'libapp/signup.html',context)

#    elif request.POST.get('test')=='test':
#        if request.user.is_authenticated:
#            return HttpResponse('true!')
#        else:
#            return HttpResponse(request.user)

def borrow(request,borrow):
    if borrow == 'borrow':
        pass
    elif borrow == 'return':
        pass
    elif borrow =='':
        if request.method == 'GET':
            username = request.user.username
            context = {
                'status' : 'get',
                'username': username,
            }
            return render(request, context)
        elif request.method == 'POST':
            pass
        pass