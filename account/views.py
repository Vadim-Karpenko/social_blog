from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Contact
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, SearchUsersForm
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from django.http import JsonResponse
from django.db.models import Q
import operator
from functools import reduce

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

class UserDetail(DetailView):
    model = User
    slug_field = 'username'

class UserList(ListView):

    """
    Display a Blog List page filtered by the search query.
    """
    model = User
    paginate_by = 30

    def get_queryset(self):
        result = super(UserList, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(username__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(first_name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(last_name__icontains=q) for q in query_list))
            )

        return result

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_username = request.POST.get('id')
    action = request.POST.get('action')
    if user_username and action:
        try:
            user = get_object_or_404(User, username=user_username)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
