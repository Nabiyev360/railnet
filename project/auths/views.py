from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View


class LoginView(View):
    def get(self, request):
        return render(request, 'auths/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        authenticated = authenticate(username=username, password=password)
        if authenticated:
            login(request, authenticated)
            if request.user.profile.role.name == 'Safety Engineer':
                return redirect('/safety/misconducts')
            elif request.user.profile.role.name == 'HR':
                return redirect('/hr/misconducts')
            else:
                return redirect('/safety/misconducts')
        else:
            return redirect('/auths/login')


def logout_view(request):
    logout(request)
    return redirect('/auths/login')