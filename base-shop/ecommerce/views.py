from django.shortcuts import render
from django.views.generic import ListView

from inventory.models import Category


def index(request):
    return render(request, "index.html")


class CategoryList(ListView):

    model = Category
    template_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


def home(request):
    return render(request, 'home.html')
