from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Repo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deep_link = models.URLField(max_length=500)
    relative_dir = models.CharField(max_length=32)

    def __str__(self):
        return self.deep_link


class Result(models.Model):
    repo = models.OneToOneField(Repo, on_delete=models.CASCADE)
    result_file = models.FileField(upload_to='results/')

    def __str__(self):
        return self.repo.deep_link


class Category(models.Model):
    results = models.ManyToManyField(Result)
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
