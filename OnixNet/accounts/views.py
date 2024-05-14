from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from website.recommend import Recommend

recommend = Recommend()


class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)


        return HttpResponseRedirect("/")
