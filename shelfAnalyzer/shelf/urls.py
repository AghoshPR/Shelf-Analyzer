
from django.urls import path
from .views import ShelfAnalysisView


urlpatterns = [
    
    path('shelf/analyze/', ShelfAnalysisView.as_view(), name='shelf-analyze'),
]
