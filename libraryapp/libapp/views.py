from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login

from libapp.models import bookModel, borrowModel

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from libapp.serializer import bookSerializer, borrowSerializer

# Create your views here.

def authorized(request):
    if not request.headers["Authorization"].split(" "):
        return False
    in_tkn = request.headers["Authorization"].split(" ")
    if not Token.objects.filter(key=in_tkn[1] if in_tkn[0] == "Token" else None):
        return False
    tkn = Token.objects.get(key=in_tkn[1] if in_tkn[0] == "Token" else None)
    if not User.objects.get(username=tkn.user.username):
        return False
    return tkn.user


@api_view(["POST","GET"])
def login(request):
    if 'username' not in request.POST or 'password' not in request.POST:
        return Response({'status' : 'not loggedin','message' : "Your Username and Password didn't match."})
    username = request.POST['username']
    password = request.POST['password']
    if User.objects.get(username=username).check_password(password):
        user = User.objects.get(username=username)
        tkn = Token.objects.get(user=user).key
        
        return Response({'status': 'logged in', 'message' : 'your loggedin','Token' : tkn})
    else:
        return Response({'status' : 'not loggedin','message' : "Your Username and Password didn't match."})
## TODO reset token

@api_view(['POST'])
def signup(request):
    for arg in ['Fname', 'Lname','email','username','password']:
        if arg not in request.POST:
            return Response({'status' : 'not logged in', 'message' : f'try agin, {arg} is not found'})
    Fname = request.POST.get('Fname')
    Lname = request.POST.get('Lname')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username):
        ##TODO  send Email and verifying email address
        User.objects.create_user(last_name=Lname,first_name=Fname ,username=username, email=email,password=password)
        newuser = User.objects.get(username=username)
        token = Token.objects.create(user=newuser)

        return Response({'status':'not logged in', 'message':'user created successfuly!', 'TOKEN' : f'{token}'})
    else: 
        return Response({'status' : 'not Login', 'message' : "your username is not available"})

## TODO func delete user
      
@api_view(["POST","GET"])
def search(request):
    ## TODO search with other fields
    if not authorized(request):
        return Response({'Detaile' : 'Access Denied'})
    if request.method == 'POST':
        search_word = request.POST['search']
        search_cases = bookModel.objects.filter(title=search_word)
        if search_cases:
            SRList = [bookSerializer(search_case).data for search_case in search_cases]
        else:
            SRList = ""
        context = {
            'SRList' : SRList,
            'username' : authorized(request).username
        }
        return Response(context)

@api_view(["POST","GET"])
def borrow(request):
    if request.method == "POST":
        Buser = authorized(request)
        bookID = request.POST['bookID']
        allfild = True if False not in [Buser, bookID] else False
        if not allfild:
            return Response({'message':'your request most have "bookID" & correct Token header'})
        Bbook = bookModel.objects.get(bookID=bookID)
        if Bbook.bookcounter < 1:
            return Response({'message' : 'this book is not available in repositorys'})

        borrowdate = request.POST['Bdate'] if 'Bdate' in request.POST else None
        returndate = request.POST['Rdate'] if 'Rdate' in request.POST else None 
        if borrowdate and returndate:
            borrowModel.objects.create(Bbook=Bbook,Buser=Buser,borrowdate=borrowdate,returndate=returndate)
        elif borrowdate and not returndate:
            borrowModel.objects.create(Bbook=Bbook,Buser=Buser,borrowdate=borrowdate)
        elif not borrowdate and returndate:
            borrowModel.objects.create(Bbook=Bbook,Buser=Buser,returndate=returndate)
        elif not borrowdate and not returndate:
            borrowModel.objects.create(Bbook=Bbook,Buser=Buser)
        Bbook.bookcounter -= 1
        Bbook.save()
        borrow = borrowModel.objects.get(Bbook=Bbook,Buser=Buser)
        return Response({'message' : 'The book borrowed to you', 'borrow': borrowSerializer(borrow).data})
    elif request.method == "GET":
        auth = authorized(request)
        if auth:
            borrowedList = borrowModel.objects.filter(Buser=auth) 
            return Response({'message' : 'authorized','borrowList' : [borrowSerializer(borrowed).data for borrowed in borrowedList]})
        return Response({'message' : 'not authorized'})

@api_view(['POST'])
def returnbook(request):
    if request.method == "POST":
        if not authorized(request):
            return Response({'message': 'your not Authorized'})
        borrowID = request.POST['borrowID']
        auth = authorized(request)
        if not request.POST['borrowID'] or not borrowModel.objects.get(borrowID=borrowID, Buser=auth):
            return Response({'message': 'borrow is not exist'})
        borrow = borrowModel.objects.get(borrowID=borrowID, Buser=auth)
        book = borrow.Bbook
        book.bookcounter += 1
        book.save()
        borrow.delete()
        return Response({'message': 'books returned'})
    





##TODO show books borrowed with user 