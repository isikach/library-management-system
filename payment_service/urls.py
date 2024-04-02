from django.urls import include, path
from rest_framework import routers

from payment_service.views import PaymentViewSet

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet, basename="payment")


urlpatterns = [
    path("", include(router.urls))
]

app_name = "payment_service"
