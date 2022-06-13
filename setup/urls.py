from venv import create
from django.contrib import admin
from django.urls import path, include
from cupom.views import RecordsViewSet, novoCupom, validarCupomQrcode, validarCupomText
from rest_framework import routers

router = routers.DefaultRouter()
router.register('records', RecordsViewSet, basename='Records')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('novo-cupom/', novoCupom),
    path('validar-cupom-nome/', validarCupomText),
    path('validar-cupom-qrcode/', validarCupomQrcode),
]
