from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import User
from cargo_app.models import CorporateUser, Shipment
from IPython import embed # type: ignore

def edituser(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id=pk)
        return render(request, 'users/edituser.html', {'userid': request.COOKIES.get('userid'), 'user': user})
    elif request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exclude(id=pk).exists():
            return render(request, "users/edituser.html", {'userid': request.COOKIES.get('userid'), 'message': 'Email has already been used.', 'messagetype': 2})
        User.objects.filter(id=pk).update(
            name=params["uname"],
            surname=params["sname"],
            password=params["passwd"],
            telephone=params["telno"],
            email=params["mail"]
        )
        return redirect(f'/users/profile/{pk}/')

def adduser(request):
    if request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exists():
            return render(request, "users/adduser.html", {'userid': request.COOKIES.get('userid'), 'message': 'Email has already been used.', 'messagetype': 2})
        user = User.objects.create(
            name=params["uname"],
            surname=params["sname"],
            password=params["passwd"],
            telephone=params["telno"],
            email=params["mail"]
        )
        return redirect(f'/users/profile/{user.id}/')
    return render(request, "users/adduser.html", {'userid': request.COOKIES.get('userid')})

def register(request):
    if request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exists():
            return render(request, "users/register.html", {'firms': CorporateUser.objects.all(), 'message': 'Email has already been used.', 'messagetype': 2})
        user = User.objects.create(
            name=params["uname"],
            surname=params["sname"],
            password=params["passwd"],
            telephone=params["telno"],
            email=params["mail"]
        )
        return redirect(f'/users/profile/{user.id}/')
    return render(request, "users/register.html")

def login(request):
    if 'userid' in request.COOKIES:
        return redirect(f'/users/profile/{request.COOKIES.get("userid")}/')
    if request.method == 'POST':
        params = request.POST
        user = User.objects.filter(email=params['mail']).first()
        if user and user.password == params['passwd']:
            response = redirect(f'/users/profile/{user.id}/')
            response.set_cookie('userid', user.id)
            return response
        return render(request, "users/login.html", {'message': 'Invalid email or password', 'messagetype': 2})
    return render(request, "users/login.html")

def details(request, pk):
    if request.method == 'GET':
        return render(request, "users/details.html", {'userid': request.COOKIES.get('userid'), 'User': User.objects.get(id=pk)})
    elif request.method == 'POST':
        params = request.POST
        User.objects.filter(id=pk).update(
            name=params['uname'],
            surname=params['sname'],
            password=params['passwd'],
            email=params['mail'],
            telephone=params['telno']
        )
        return redirect(f'/users/profile/{pk}/')

def logout(request):
    response = redirect('/users/login/')
    response.delete_cookie('userid')
    return response

def delete(request, pk):
    if request.COOKIES.get('userid') != str(pk):
        User.objects.filter(id=pk).delete()
    return redirect("/adminpanel/")

def update(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id=pk)
        return render(request, 'users/profile.html', {'userid': request.COOKIES.get('userid'), 'user': user})
    elif request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exclude(id=pk).exists():
            return render(request, "users/profile.html", {'message': 'Email has already been used.', 'messagetype': 2})
        User.objects.filter(id=pk).update(
            name=params["uname"],
            surname=params["sname"],
            password=params["passwd"],
            telephone=params["telno"],
            email=params["mail"]
        )
        return redirect(f'/users/profile/{pk}/')

def makeadmin(request, pk):
    User.objects.filter(id=pk).update(isAdmin=True)
    return redirect("/adminpanel/")
