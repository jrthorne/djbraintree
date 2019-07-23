from .views import (
    CheckoutView,
    )
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', CheckoutView.as_view(), name='checkout'),
]