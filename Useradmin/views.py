from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from .forms import MySignUpForm


class MySignUpView(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            "Dein Account wurde erstellt. "
            "Dein Accountname lautet: " + self.object.username,
        )

        return response


class MyLoginView(LoginView):
    template_name = "registration/login.html"
