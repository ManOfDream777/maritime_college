from typing import Any, Dict
from django.views.generic import TemplateView
from .models import BlogCategory, Faculty

class BlogCategoriesMixin(TemplateView):

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        return context

class FacultiesMixin(TemplateView):

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['faculties'] = Faculty.objects.all()
        return context