from django.urls import path
from .views import StockMoveListView


urlpatterns = [
    path('', StockMoveListView.as_view()),
]
