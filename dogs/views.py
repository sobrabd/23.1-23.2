from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Category, Dog, Parent
from django.urls import reverse_lazy, reverse
from .forms import DogForm, ParentForm
from django.forms import inlineformset_factory


class IndexView(TemplateView):
    template_name = 'dogs/index.html'
    extra_context = {
        'title': 'Питомник - Добро пожаловать',
    }

    def get_context_data(self, **kwargs: Any):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Питомник - Наши породы'
    }


class DogListView(ListView):
    model = Dog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['object_list'] = Dog.objects.filter(category_id=category_item.pk)
        context_data['title'] = f'Все собаки породы {category_item.name}'

        return context_data


class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy('dogs:categories')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

class DogUpdateView(UpdateView):
    model = Dog
    fields = ('name', 'category')

    def get_success_url(self):
        return reverse('dogs:category_dogs', args=[self.object.category.pk])
    
    def get_context_data(self, **kwargs: Any):
        context_data = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormSet(self.request.POST, instance=self.object)
        else:
            formset = ParentFormSet(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

class DogDeleteView(DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:categories')
