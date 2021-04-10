from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import LoginForm


class IndexView(TemplateView):
    template_name = "application.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        if user.is_anonymous:
            context["form"] = LoginForm()
            context["next"] = "/"
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            return redirect("index")
        user = form.save()
        if user is not None:
            login(request, user)
        return redirect("index")


class LogOutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("index")
