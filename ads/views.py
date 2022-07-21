import json

import pandas as pandas
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView

from Lesson28_HW import settings
from ads.models import CategoryModel, AdModel
from users.models import User


def index(request):
    response = {"status": "ok"}
    return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(ListView):
    model = CategoryModel
    queryset = CategoryModel.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")
        response = []

        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = CategoryModel
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = CategoryModel.objects.create(
            name=category_data["name"]
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


class CategoryDetailView(DetailView):
    model = CategoryModel

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = CategoryModel
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        self.object.name = category_data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = CategoryModel
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdView(ListView):
    model = AdModel
    queryset = AdModel.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('author').order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        ads = []

        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category": ad.category.name,
                "image": ad.image.url if ad.image else None
            })

        response = {
            "items": ads,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count
        }

        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = AdModel

    def get(self, request, *args, **kwargs):

        try:
            ad = self.get_object()
        except AdModel.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "image": ad.image,
            "description": ad.description,
            "price": ad.price,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = AdModel
    fields = ["name", "author", "description", "price", "is_published", "category"]

    def post(self, request, *args, **kwargs):

        ad_data = json.loads(request.body)

        author = get_object_or_404(User, id__iexact=ad_data["author_id"])
        category = get_object_or_404(CategoryModel, id__iexact=ad_data["category_id"])

        ad = AdModel.objects.create(
            name=ad_data["name"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            image=ad_data["image"],
            category=category
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = AdModel
    fields = ["name", "author", "description", "price", "category"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]

        self.object.author = get_object_or_404(User, id__iexact=ad_data["author_id"])
        self.object.category = get_object_or_404(CategoryModel, id__iexact=ad_data["category_id"])

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = AdModel
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = AdModel
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "image": self.object.image.url if self.object.image else None
        })


class AddToCat(View):
    def get(self, request):
        csv_data = pandas.read_csv('ads/data/category.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            CategoryModel.objects.create(
                name=csv_data["name"][i],
            )
            i += 1

        return JsonResponse("Записи добавлены в указанную таблицу!", safe=False, status=200)


class AddToAd(View):
    def get(self, request):
        csv_data = pandas.read_csv('ads/data/ad.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['Id'].keys()) >= i:
            AdModel.objects.create(
                name=csv_data["name"][i],
                author_id=csv_data["author_id"][i],
                price=csv_data["price"][i],
                description=csv_data["description"][i],
                is_published=csv_data["is_published"][i],
            )
            i += 1

        return JsonResponse("Записи добавлены в указанную таблицу!", safe=False, status=200)
