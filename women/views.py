from typing import Any
from django.db.models.base import Model as Model
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from .utils import *
from django.core.paginator import Paginator
from django.core.cache import cache

from .models import Women, Category, TagPost, UploadFiles
from .forms import AddPostForm, ContactForm

import uuid


data_db = [
    {'id': 1, 'title': 'Lolly Lips', 'content': '''<h1>Lolly Lips</h1>(настоящее имя Настя Солодкова) – высокорейтинговая актриса из России, работающая на съемках видео откровенного характера. Популярная благодаря оригинальному подходу к режиссуре домашнего «18+» материала.''', 'is_published': True},
    {'id': 2, 'title': 'Sweety Fox', 'content': 'Биография Sweety Fox', 'is_published': False},
    {'id': 3, 'title': 'Lana Rhoades', 'content': 'Биография Lana Rhoades', 'is_published': True},
]

class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
        
    def get_queryset(self):
        w_lst = cache.get('women_posts')
        if not w_lst:
            w_lst = Women.published.all().select_related('cat')
            cache.set('women_posts', w_lst, 60)

        return w_lst

# Загрузка файлов на сервер-----------------------
@login_required
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html',{'title': 'О сайте', 'page_obj': page_obj})

#-------------------------------------------------

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title = context['post'])
    
    def get_object(self, queryset = None):
        return get_object_or_404(Women.published, slug = self.kwargs[self.slug_url_kwarg])

# Добавление новой записи на сайт--------------------------------------------------
class AddPage(PermissionRequiredMixin, DataMixin, CreateView,):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'
    permission_required = 'woemn.add_women'
    
    def form_valid(self, form):
        w = form.save(commit = False)
        w.author = self.request.user
        return super().form_valid(form)
# -------------------------------------------------------------------------------

class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = '__all__'
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    permission_required = 'women.change_women'

# Создание каптчи для сайта-------------------------------------------------------------------
class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    
# --------------------------------------------------------------------------------------------
def login(request):
    return HttpResponse("Авторизация")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена </h1>")

# Класс представления для категорий-----------------------------------------------------------
class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False
    
    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.filter(cat__slug = self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            cat = context['posts'][0].cat
            return self.get_mixin_context(context, title = 'Каетгория - ' + cat.name, cat_selected = cat.id,)
#----------------------------------------------------------------------------------------------


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
    
# Создание каптчи для сайта-------------------------------------------------------------------

# --------------------------------------------------------------------------------------------