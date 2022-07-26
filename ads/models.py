from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import CASCADE, SET_NULL

from users.models import User


class CategoryModel(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(5)])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class AdModel(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(10)])
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_published = models.BooleanField(default=False)
    description = models.TextField(max_length=1000, null=True, blank=True)

    image = models.ImageField(upload_to="ads/", null=True, blank=True)

    author = models.ForeignKey(User, on_delete=CASCADE)
    category = models.ForeignKey(CategoryModel, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    list_of_ads = models.ManyToManyField(AdModel)

    class Meta:
        verbose_name = "Выборка"
        verbose_name_plural = "Выборки"

    def __str__(self):
        return self.name
