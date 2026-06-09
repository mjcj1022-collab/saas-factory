from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, DrawingViewSet, RevisionAnalysisViewSet, TradePackageViewSet, PunchItemViewSet, DailyReportViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("drawings", DrawingViewSet, basename="drawing")
router.register("revisions", RevisionAnalysisViewSet, basename="revision")
router.register("trades", TradePackageViewSet, basename="trade")
router.register("punch-items", PunchItemViewSet, basename="punch")
router.register("daily-reports", DailyReportViewSet, basename="daily-report")

urlpatterns = [path("", include(router.urls))]
