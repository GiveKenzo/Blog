from django.contrib.auth import authenticate, login, logout
from .forms import LoginUserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model

from sitewomen import settings

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}
    
    # def get_success_url(self) -> str:
    #     return reverse_lazy('home')
    
# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username = cd['username'], password = cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
            
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))

# Регистрация новых пользователей------------------------------------------
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')
# ---------------------------------------------------------------------------

# Профиль пользователя-------------------------------------------------------
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя", 'default_image': settings.DEFAULT_USER_IMAGE}
    
    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args = [self.request.user.pk])
    
    def get_object(self, queryset = None):
        return self.request.user
# ---------------------------------------------------------------------------

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}