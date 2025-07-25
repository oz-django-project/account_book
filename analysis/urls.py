from django.urls import path

from .views import AnalysisCreateView, AnalysisListView

urlpatterns = [
    path("analysis/", AnalysisListView.as_view(), name="analysis-list"),
    path("analysis/create/", AnalysisCreateView.as_view(), name="analysis-create"),
]
