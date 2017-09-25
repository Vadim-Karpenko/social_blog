from django.shortcuts import render, redirect
from .models import Profile, Contact
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login

class User_login(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('/')
            else:
                messages.error(request, 'Disabled account')
        else:
            messages.error(request, 'Invalid login')
        return super(User_login, self).form_valid(form)
