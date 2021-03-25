from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie, Actor
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ReviewSerializer, \
    CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filters=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод деталей фильмов"""
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class ReviewView(APIView):
    """Показать отзыв"""
    def post(self, request):
        review = ReviewSerializer(data=request.data)
        return review


class AddStarRatingView(APIView):
    """Добавление рейтинга к фильму"""
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
    # def get(self, request):
    #     actors = Actor.objects.all()
    #     serializer = ActorListSerializer(actors, many=True)
    #     return Response(serializer.data)


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
    # def get(self, request, pk):
    #     actors = Actor.objects.get(id=pk)
    #     serializer = ActorDetailSerializer(actors)
    #     return Response(serializer.data)
