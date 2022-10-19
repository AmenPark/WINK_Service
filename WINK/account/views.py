from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
import re

def signupUser(request):
    form = UserCreationForm
    context = {"form" : form}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("된건가?")
            print(form.password)
            # user = form.save()
            # login(request,user)
            # return redirect('Routine:memo')
            render(request, 'account/signup.html', context)
    else:
        form = UserCreationForm()
    context = {"form":form}
    return render(request, 'account/signup.html', context)

def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('Routine:memo')  # 로그인 성공시 메인페이지 이동
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'account/login.html', context)

# Create your views here.
