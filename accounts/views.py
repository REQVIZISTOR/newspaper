from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import CustomSignupForm  # обновленный импорт

class SignUp(CreateView):
    model = User
    form_class = CustomSignupForm  # обновленное использование формы
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

# Create your views here.
