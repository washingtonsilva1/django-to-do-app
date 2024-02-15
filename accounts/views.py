import sweetify
from forms import LoginForm, RegisterForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginTemplateView(TemplateView):
    template_name = 'accounts/view/login.html'

    def get(self, req, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todoapp:home')
        return super().get(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        form = LoginForm(self.request.POST or None)
        if form.is_valid():
            user_auth = authenticate(
                self.request,
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', ''),
            )
            if user_auth is not None:
                sweetify.toast(
                    self.request,
                    'You have been logged in successfully!',
                    icon='success'
                )
                login(self.request, user_auth)
                return redirect('todoapp:home')
            else:
                sweetify.error(
                    self.request,
                    title='User not found',
                    text='Incorrect username or password.',
                    persistent='Close'
                )
                return redirect('accounts:login')
        else:
            return self.get(req, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = LoginForm(self.request.POST or None)
        ctx.update({
            'title': 'Login',
            'form': form,
        })
        return ctx


class RegisterTemplateView(TemplateView):
    template_name = 'accounts/view/register.html'

    def get(self, req, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todoapp:home')
        return super().get(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        form = RegisterForm(self.request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            sweetify.toast(
                self.request,
                'Your user has been created successfully!',
                icon='success',
            )
            return redirect('accounts:login')
        return self.get(req, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = RegisterForm(self.request.POST or None)
        ctx.update({
            'form': form,
            'title': 'Register',
        })
        return ctx


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def post(self, req, *args, **kwargs):
        u = self.request.POST.get('user', None)
        if u is None or u is not None and \
                not u == self.request.user.get_username():
            return redirect('todoapp:home')
        logout(self.request)
        sweetify.toast(
            self.request,
            'You have been logged out successfully!',
            icon='success'
        )
        return redirect('accounts:login')
