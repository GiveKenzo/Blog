from django.db import models
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import get_user_model

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_published = Women.Status.PUBLISHED)
    
    
class Women(models.Model): 
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length = 255)
    slug = models.SlugField(max_length = 255, unique = True, db_index = True, validators = [
        MinLengthValidator(5),
        MaxLengthValidator(100),
    ])
    content = models.TextField(blank = True)
    time_create = models.DateTimeField(auto_now_add = True)
    time_update = models.DateTimeField(auto_now = True)
    is_published = models.BooleanField(choices = tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default = Status.DRAFT)
    cat = models.ForeignKey("Category", on_delete = models.PROTECT, related_name = 'posts')
    tags = models.ManyToManyField('TagPost', blank = True, related_name = 'tags') #Связь ManyToMany c классом TagPost
    husband = models.OneToOneField('Husband', on_delete = models.SET_NULL, null = True, blank = True, related_name = 'wuman')
    #Поле загрузки фото к постам____________________________________________
    photos = models.ImageField(upload_to = "photos/%Y/%m/%d/", default = None, blank = True, null = True, verbose_name = "Фото")
    #-----------------------------------------------------------------------
    # Добавление автора статьи----------------------------------------------
    author = models.ForeignKey(get_user_model(), on_delete = models.SET_NULL, related_name = 'posts', null = True, default = None)
    # ----------------------------------------------------------------------
    
    objects = models.Manager()
    published = PublishedManager()
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Известные порноактрисы"
        verbose_name_plural = "Известные порноактрисы"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields = ['-time_create']),
    ]
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    # def save(self, *args, **kwargs): #Правильно сохранение записи в админке без костылей
    #     self.slug = slugify(unidecode(str(self.title)))
    #     super().save(*args, **kwargs)
    
class Category(models.Model): # Делаем связь Many To One 
    name = models.CharField(max_length = 100, db_index = True)
    slug = models.SlugField(max_length = 100, unique = True, db_index = True)
    
    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("category", kwargs={'cat_slug': self.slug})
    
    
class TagPost(models.Model):         #Связь ManyToMany 
    tag = models.CharField(max_length = 100, db_index = True)
    slug = models.SlugField(max_length = 255, unique = True, db_index = True)
    
    def __str__(self):               #Возвращает название тэга
        return self.tag
    
    def get_absolute_url(self): 
        return reverse("tag", kwargs={'tag_slug': self.slug})
    
class Husband(models.Model):         # Связь One To One
    name = models.CharField(max_length = 100)
    age = models.IntegerField(null = True)
    m_count = models.ImageField(blank = True, default = 0)
    
    def __str__(self):
        return self.name
    

#Хранение ссылок на загруженные файлы--------------------
class UploadFiles(models.Model):
    file = models.FileField(upload_to = 'uploads_model')
#--------------------------------------------------------