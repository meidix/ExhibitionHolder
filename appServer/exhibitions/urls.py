from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register('exhibition', views.ExhibitionViewSet)
router.register('visitors', views.VisitorViewSet)

visitor_create = views.VisitorViewSet.as_view({
    'post': "create"
})

urlpatterns = [
    path('', include(router.urls)),
    path('visitor/<pk>/', visitor_create),
    path('options/coops/', views.CoopRequestListAPIView.as_view()),
    path("options/products/", views.ProductListAPIView.as_view())
]