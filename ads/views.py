import json

import pandas as pandas
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from Lesson28_HW import settings
from ads.models import CategoryModel, AdModel, Selection
from ads.permissions import AdUpdatePermission, SelectionUpdatePermission
from ads.serializers import AdSerializer, SelectionListSerializer, SelectionSerializer, SelectionDetailSerializer
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


class AdView(ListAPIView):
    model = AdModel
    queryset = AdModel.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        categories = request.GET.getlist("cat", [])
        if categories:
            self.object_list = self.object_list.filter(category_id__in=categories)

        if request.GET.get("text", None):
            self.object_list = self.object_list.filter(name__icontains=request.GET.get("text"))

        if request.GET.get("location", None):
            self.object_list = self.object_list.filter(author__locations__name__icontains=request.GET.get("location"))

        if request.GET.get("price_from", None):
            self.object_list = self.object_list.filter(price__gte=request.GET.get("price_from"))

        if request.GET.get("price_to", None):
            self.object_list = self.object_list.filter(price__lte=request.GET.get("price_to"))

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


# class AdDetailView(RetrieveAPIView):
#     queryset = AdModel.objects.all()
#     serializer_class = AdSerializer
#     permission_classes = [IsAuthenticated]
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ad_detail(request):
    try:
        ad_id = request.GET.get("id")
        ad = AdModel.objects.filter(pk=ad_id)
    except AdModel.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    return JsonResponse({
        "id": ad.id,
        "name": ad.name,
        "author": ad.author,
        "address": ad.address,
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


class AdUpdateView(UpdateAPIView):
    queryset = AdModel.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdUpdatePermission]


class AdDeleteView(DestroyAPIView):
    queryset = AdModel.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdUpdatePermission]


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


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionRetrieveView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


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
