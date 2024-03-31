from django import forms
from .models import Category, Husband, Women
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#     code = 'russian'

#     def __init__(self, message = None):
#         self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

#     def __call__(self, value, *args, **kwwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code = self.code, params = {"value": value})

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset = Category.objects.all(), empty_label = "Категория не выбрана", label = "Категории")
    husband = forms.ModelChoiceField(queryset = Husband.objects.all(), required = False, empty_label = "Не замужем", label = "Муж")

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photos', 'is_published', 'cat', 'husband', 'tags']
        widget = {
            'title': forms.TextInput(attrs = {'class': 'form-input'}),
            'content': forms.TextInput(attrs = {'cols': 60, 'rows': 10}),
        }
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

# Параметра загрузки файла, здесь стоит только изображение----------------------
class UploadFileForm(forms.Form):
    file = forms.ImageField(label = "Изображение")
# ------------------------------------------------------------------------------

# Каптча------------------------------------------------------------------------
class ContactForm(forms.Form):
    captcha = CaptchaField()
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}), label = 'Сообщение об ошибке')
# ------------------------------------------------------------------------------