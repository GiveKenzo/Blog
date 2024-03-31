menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
    title_page = None
    extra_context = {}
    paginate_by = 3
    
    def __init__(self) -> None:
        if self.title_page:
            self.extra_context['title'] = self.title_page
        

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        context['cat_selected'] = None
        context.update(kwargs)
        return context