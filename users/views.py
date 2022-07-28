import pandas as pandas

from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Location
from users.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer, \
    LocationSerializer


class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # models = User
    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     self.object_list = self.object_list.annotate(total_ads=Count('ad'))
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_num = request.GET.get('page')
    #     page_obj = paginator.get_page(page_num)
    #
    #     users = []
    #     for user in page_obj:
    #         users.append({
    #             "id": user.id,
    #             "username": user.username,
    #             "first_name": user.first_name,
    #             "last_name": user.last_name,
    #             "role": user.role,
    #             "age": user.age,
    #             "total_ads": user.total_ads,
    #             "location": list(map(str, user.locations.all()))
    #         })
    #
    #     response = {
    #         "items": users,
    #         "num_pages": page_obj.paginator.num_pages,
    #         "total": page_obj.paginator.count
    #     }
    #
    #     return JsonResponse(response, safe=False,)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class AddToLocation(View):

    def get(self, request):
        csv_data = pandas.read_csv('users/data/location.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            Location.objects.create(
                name=csv_data["name"][i],
                lat=csv_data["lat"][i],
                lng=csv_data["lng"][i],
            )
            i += 1

        return JsonResponse({"status": "ok"}, status=200)


class AddToUser(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def get(self, request):
        csv_data = pandas.read_csv('users/data/user.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            try:
                location_obj = Location.objects.get(id=csv_data["location_id"][i])
            except Location.DoesNotExist:
                return JsonResponse({"status": "Location don't found"}, status=404)

            print("***")
            print(dir(location_obj))
            print("***")

            new_user = User.objects.create(
                first_name=csv_data["first_name"][i],
                last_name=csv_data["last_name"][i],
                username=csv_data["username"][i],
                password=csv_data["password"][i],
                role=csv_data["role"][i],
                age=csv_data["age"][i],
            )
            new_user.locations.add(location_obj)
            i += 1

        return JsonResponse({"status": "ok"}, status=200)
