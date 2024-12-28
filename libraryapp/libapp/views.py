from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return HttpResponse('')
@csrf_exempt
#request={"status" : "login/signup", 'username':'UN', password:'PW', 'fname' : 'fname', 'lname': 'lname', 'email':'email', }
def login(request):
    if request.POST.get('status') == 'login':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.get(username=username) and User.objects.get(username=username).check_password(password):
            request.session['user_id'] = User.objects.get(username=username).id
            request.User
            context = {
                'page': 'login',
                'st' : 'loggedin',
                'msg' : "You're logged in."
            }
            return HttpResponse("You're logged in.")
            #return render(request,context)
        else:
            context = {
                'page' : 'login',
                'st' : 'not login',
                'msg' : "Your Username and Password didn't match."
            }
            return HttpResponse("Your Username and Password didn't match.")
            #return render(request,context)
    elif request.POST.get('status') == 'signup':
        Fname = request.POST.get('Fname')
        lname = request.POST.get('Lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.get(username=username):
            ##TODO: send Email and verifying email address
            newusr = User.objects.create_user(username=username, email=email,password=User.set_password(password))
            newusr.first_name = Fname
            newusr.last_name = lname
            newusr.save()
