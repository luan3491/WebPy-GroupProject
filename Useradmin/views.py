from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .forms import MySignUpForm, ProfileUpdateForm


class MySignUpView(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            _("Your account has been created. Your account name is: %(username)s")
            % {"username": self.object.username},
        )

        return response


class MyLoginView(LoginView):
    template_name = "registration/login.html"


@login_required
def profile_settings(request):
    profile_form = ProfileUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=request.user,
            )

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, _("Your profile has been updated."))
                return redirect("profile_settings")

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, _("Your password has been changed."))
                return redirect("profile_settings")

    return render(
        request,
        "registration/profile_settings.html",
        {
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )
