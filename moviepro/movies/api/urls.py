from django.urls import path
from movies.api import views as api_views


urlpatterns = [
    path('movies/', api_views.MovieListCreateAPIView.as_view(), name='movies'),
    path('movies/<int:pk>/', api_views.MovieDetailAPIView.as_view(), name='movies-detail'),
]
