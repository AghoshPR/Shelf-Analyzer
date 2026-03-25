
from django.urls import path
from .views import ShelfAnalysisView


urlpatterns = [
    
    path('analyze/',ShelfAnalysisView.as_view(),name='shelf-analyze')
]
