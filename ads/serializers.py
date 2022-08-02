from rest_framework import serializers

from ads.models import AdModel, Selection


class AdSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        model = AdModel
        fields = ["id", "name", "price", "description", "author", "category"]


class SelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)
    owner = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Selection
        fields = '__all__'
