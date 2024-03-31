from django.contrib import admin, messages
from .models import Women, Category
from django.utils.safestring import mark_safe

class MarriedFilter(admin.SimpleListFilter): #Добавление собственного фильтра
    title = 'Статус женщин'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]
        
    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull = False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull = True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('title', 'photos', 'post_photos', 'time_create', 'is_published', 'cat')
    readonly_fields = ['post_photos']
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    list_per_page =  10
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name'] #Добавляю панель поиска и поиск по категориям
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] #панель для фильтрации
    fields = ['title', 'content', 'photos', 'slug', 'cat', 'husband', 'tags']
    readonly_fields = ['slug']
    filter_vertical = ['tags']
    save_on_top = True

# Отображение фото в админке-------------------------------------------------
    @admin.display(description = "Изображение", ordering = 'content')
    def post_photos(self, women: Women):
        if women.photos:
            return mark_safe(f"<img src = '{women.photos.url}' width = 50>")
        return "Без фото"
# ---------------------------------------------------------------------------

    @admin.action(description = "Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published = Women.Status.PUBLISHED) #Он принимает два дополнительных параметра requets объект запроса, queryset - объект с выбранными записями. Заетм используя набор записей мы для них вызываем метод update()
        self.message_user(request, f"Изменено {count} записи(ей)")# и изменем поле паблишед на значение ПАБЛИШЕД    


    @admin.action(description = "Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published = Women.Status.DRAFT)
        self.message_user(request, f"{count} снято с публикации", messages.WARNING)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


#admin.site.register(Women, WomenAdmin)


