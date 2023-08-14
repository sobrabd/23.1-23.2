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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dogs/index.html'
    extra_context = {
        'title': 'Питомник - Добро пожаловать',
    }

    def get_context_data(self, **kwargs: Any):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    extra_context = {
        'title': 'Питомник - Наши породы'
    }


class DogListView(LoginRequiredMixin, ListView):
    model = Dog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            category_id=self.kwargs.get('pk')
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'Все собаки породы {category_item.name}'

        return context_data


class DogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy('dogs:categories')
    permission_required = 'dogs.add_dog'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    fields = ('name', 'category')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

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


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:categories')
