from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

def signupUser(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            request.session['id'] = user.id
            return redirect('/Routine/')
    else:
        form = UserCreationForm()
    context = {"form":form}
    return render(request, 'account/signup.html', context)

def loginUser(request):
    if request.user.id != None:
        return logoutUser(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            user = form.get_user()
            return redirect('/Routine/')  # 로그인 성공시 메인페이지 이동
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'account/login.html', context)

def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/Routine/')
    else:
        return render(request, 'account/logout.html',{})

# Create your views here.
