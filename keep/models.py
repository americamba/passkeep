from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        ordering = ["name", ]
        verbose_name_plural = "categories"

    name = models.CharField(max_length=25, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_category')

    def __str__(self):
        return self.name


class Password(models.Model):

    class Meta:
        ordering = ["title", "username"]

    title = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    url = models.URLField(null=True, blank=True, verbose_name="URL")
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_account')

    def __str__(self):
        return self.title
