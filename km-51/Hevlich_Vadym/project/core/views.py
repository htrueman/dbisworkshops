import os
import random
import re
import string
import subprocess
import sys

import auger
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.conf import settings

from git import Repo as GitRepo

from .forms import AddRepoForm, AddCategoryForm, UpdateCategoryForm
from .models import Repo, Category, Result


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('core:main')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class MainView(CreateView, ListView):
    template_name = 'main.html'
    success_url = reverse_lazy('core:main')
    form_class = AddRepoForm

    def get_queryset(self):
        return Repo.objects.filter(user=self.request.user)

    def form_valid(self, form):
        repo = form.save(commit=False)
        repo.user = self.request.user

        repo_dir = ''.join(random.choice(string.ascii_letters + string.digits)
                           for _ in range(10))
        repo.relative_dir = repo_dir

        repo.save()

        GitRepo.clone_from(repo.deep_link, os.path.join(settings.REPOS_DIR, repo_dir))
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'object_list': self.get_queryset})


def main():
    v = MainView()


class RepoView(DetailView):
    model = Repo
    template_name = 'repo.html'
    success_url = reverse_lazy('core:main')

    @staticmethod
    def make_import(name):
        mod = __import__(name)
        class_name = getattr(mod, name.split('.')[-1])
        return class_name

    def findfiles(self, path, dir_name):
        for path, dirs, files in os.walk(path):
            for filename in files:
                if '.py' in filename:
                    fullpath = os.path.join(path, filename)
                    with open(fullpath, 'r') as f:
                        context_lines = f.readlines()
                        for line in context_lines:
                            if '# test_magic' in line:
                                mod_name = fullpath.split('/')[-2:]
                                last_mod_name = mod_name[-1].split('.')[0]
                                python_mod_name = '.'.join(mod_name[:-1])
                                python_mod_name = python_mod_name + '.' + last_mod_name

                                sys.path.insert(0, '/'.join(fullpath.split('/')[:-2]))

                                class_name = line.lstrip('class ').split('(')[0]

                                module = self.make_import(python_mod_name + '.' + class_name)
                                return module

    def get(self, request, *args, **kwargs):
        if 'remove' in request.GET.keys():
            self.get_object().delete()
            return redirect(self.success_url)
        elif 'generate' in request.GET.keys():
            # module = self.findfiles(
            #     os.path.join(settings.REPOS_DIR, self.get_object().relative_dir), self.get_object().relative_dir)

            subprocess.run(["python",
                            "{}/run.py".format(os.path.join(settings.REPOS_DIR, self.get_object().relative_dir))])
            from os import listdir
            from os.path import isfile, join
            path = "{}/tests".format(os.path.join(settings.REPOS_DIR, self.get_object().relative_dir))
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

            res = open("{}/tests/{}".format(
                os.path.join(settings.REPOS_DIR, self.get_object().relative_dir),
                onlyfiles[0]))
            try:
                res_obj = Result.objects.get(repo=self.get_object())
                res_obj.result_file = File(res)
                res_obj.save()
            except Result.DoesNotExist:
                res_obj = Result.objects.create(repo=self.get_object(), result_file=File(res))
            res.close()
            return FileResponse(open(res_obj.result_file.path, 'rb'), as_attachment=True, filename='test.py')
        elif 'update' in request.GET.keys():
            repo = GitRepo(os.path.join(settings.REPOS_DIR, self.get_object().relative_dir))
            o = repo.remotes.origin
            o.pull()

        return super().get(request, *args, **kwargs)


class CategoriesView(CreateView, ListView):
    model = Category
    template_name = 'categories.html'
    form_class = AddCategoryForm
    success_url = reverse_lazy('core:categories')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user
        category.save()
        return redirect(self.success_url)


class CategoryView(UpdateView, DetailView):
    model = Category
    template_name = 'category.html'
    form_class = UpdateCategoryForm
    success_url = reverse_lazy('core:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = Result.objects.all()
        return context
