from django.contrib.auth.models import User
from libapp.models import bookModel, borrowModel
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from libapp.serializer import bookSerializer, borrowSerializer, userSerializer


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

def checkargs(request,l=list, all=True):
    if all:
        return False if False in [True if request.POST.get(i) else False for i in l] else True
    else:
        return False if True not in [True if request.POST.get(i) else False for i in l] else True



@api_view(["POST","GET"])
def login(request):
    if checkargs(request,['username','password']):
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
    if checkargs(request, ['Fname', 'Lname','email','username','password']):
        return Response({'status' : 'not logged in', 'message' : f'try agin, some fields not found'})
    Fname = request.POST.get('Fname')
    Lname = request.POST.get('Lname')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username):
        ##TODO  send Email and verifying email address
        User.objects.create_user(last_name=Lname, first_name=Fname, username=username, email=email, password=password)
        newuser = User.objects.get(username=username)
        token = Token.objects.create(user=newuser)
        return Response({'status':'not logged in', 'message':'user created successfuly!', 'Token' : f'{token}'})
    else: 
        return Response({'status' : 'not logged in', 'message' : "your username is not available"})

#api/Users/
@api_view(["GET"])
def UsersList(request):
    if authorized(request).is_staff:
        return Response({'users':[userSerializer(user).data for user in User.objects.all()]})
    else:
        return Response({'message':'Access Denied'})

@api_view(["POST"])
def deleteUser(request):
    if authorized(request).is_staff:
        if not request.POST['userID']:
            return Response({'message': 'set the userID'})
        user = User.objects.get(id=request.POST.get('userID'))
        userserial = userSerializer(user).data
        user.delete()
        return Response({'message':f'{userserial} deleted'})
    else:
        return Response({'message':'Access Denied'})


#api/books/
@api_view(["POST"])
def addbook(request):
    if not checkargs(request,['author', 'title', 'year', 'publisher']):
        return Response({'message':'some fields not found!'})
    elif not authorized(request).has_perm('libapp.libperm'):
        return Response({'message': 'Access Denied'})
    author = request.POST['author']
    title = request.POST['title']
    year = request.POST['year']
    publisher = request.POST['publisher']
    if bookModel.objects.filter(author=author, title=title, year=year, publisher=publisher):
        return Response({'message': 'this book is alredy exist!'})
    if request.POST.get('bookcounter'):
        bookcounter = request.POST['bookcounter']
        bookModel.objects.create(author=author, title=title, year=year, publisher=publisher, bookcounter=bookcounter)
    else:
        bookModel.objects.create(author=author, title=title, year=year, publisher=publisher)

@api_view(["POST","GET"])
def search(request):
    if request.method == 'POST':
        if not checkargs(request,['bookID','author','title','year','poblisher'],False): 
            return Response({"message": 'fill some field to search'})
        search_word = [request.POST[x] if x in request.POST else"" for x in ['bookID','author','title','year','poblisher']]
        if 'gte' in search_word[3]:
            search_cases = bookModel.objects.filter(bookID__icontains=search_word[0],
                                                    author__icontains=search_word[1],
                                                    title__icontains=search_word[2],
                                                    year__gte=search_word[3].split('-')[1],
                                                    publisher__icontains=search_word[4],
                                                    )
        elif 'lte' in search_word[3]: 
            search_cases = bookModel.objects.filter(bookID__icontains=search_word[0],
                                                    author__icontains=search_word[1],
                                                    title__icontains=search_word[2],
                                                    year__lte=search_word[3].split('-')[1],
                                                    publisher__icontains=search_word[4],
                                                    )
        else: 
            search_cases = bookModel.objects.filter(bookID__icontains=search_word[0],
                                                    author__icontains=search_word[1],
                                                    title__icontains=search_word[2],
                                                    year__icontains=search_word[3],
                                                    publisher__icontains=search_word[4],
                                                    )

        SRList = [bookSerializer(search_case).data for search_case in search_cases] if search_cases else ""
        context = {
            'SRList' : SRList,
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
            borrow = borrowModel.objects.create(Bbook=Bbook,Buser=Buser,borrowdate=borrowdate,returndate=returndate)
        elif borrowdate and not returndate:
            borrow = borrowModel.objects.create(Bbook=Bbook,Buser=Buser,borrowdate=borrowdate)
        elif not borrowdate and returndate:
            borrow = borrowModel.objects.create(Bbook=Bbook,Buser=Buser,returndate=returndate)
        elif not borrowdate and not returndate:
            borrow = borrowModel.objects.create(Bbook=Bbook,Buser=Buser)
        Bbook.bookcounter -= 1
        Bbook.save()
        return Response({'message' : 'The book borrowed to you', 'borrow': borrowSerializer(borrow).data})
    elif request.method == "GET":
        auth = authorized(request)
        if not auth:
            return Response({'message' : 'not authorized'})
        elif auth.has_perm('libapp.libperm'):
            borrowedList = borrowModel.objects.all() 
            return Response({'message' : 'librarian - authorized','borrowList' : [borrowSerializer(borrowed).data for borrowed in borrowedList]})
        elif auth.has_perm('libapp.normalperm'):
            borrowedList = borrowModel.objects.filter(Buser=auth) 
            return Response({'message' : 'authorized','borrowList' : [borrowSerializer(borrowed).data for borrowed in borrowedList]})

@api_view(['POST'])
def returnbook(request):
    if request.method == "POST":
        if not authorized(request) or not authorized(request).has_perm('libapp.libperm'):
            return Response({'message': 'your not Authorized'})
        if not request.POST['borrowID'] or not borrowModel.objects.get(borrowID=borrowID):
            return Response({'message': 'borrow is not exist'})
        borrowID = request.POST.get('borrowID')
        borrow = borrowModel.objects.get(borrowID=borrowID)
        book = borrow.Bbook
        book.bookcounter += 1
        book.save()
        borrow.delete()
        return Response({'message': 'book returned'})


