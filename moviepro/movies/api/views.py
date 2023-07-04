from rest_framework import generics
from movies.models import Movie
from movies.api.serializers import MovieSerializer
from movies.api.permissions import IsAdminUserOrReadOnly


class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all().order_by('id')
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]
