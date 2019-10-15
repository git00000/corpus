from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView


from .forms import LoginForm

# Create your views here.

def signin_view(request):
    return render(request, 'accounts/signin.html')

def signout_view(request):
     pass


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = "accounts/login.html"

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        print(email, password)
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.get_success_url(user=user))
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self, user=None):
        if user.is_admin:
            return reverse("myadmin:dashboard")
        
        # user is staff
        return reverse("user:profile")


def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))



        

        

