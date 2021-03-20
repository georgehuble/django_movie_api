from rest_framework import serializers

from .models import Movie, Review, Rating


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""
    class Meta:
        model = Review
        fields = '__all__'


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсии children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReviewSerializer(serializers.ModelSerializer):
    """Показать отзывы"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating
