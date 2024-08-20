from django.contrib   import admin
from django.urls      import path
from django.urls.conf import include
from rest_framework   import routers
from api              import views

router = routers.DefaultRouter()
router.register(r'secao', views.SecaoViewSet)
router.register(r'divisao', views.DivisaoViewSet)
router.register(r'grupo', views.GrupoViewSet)
router.register(r'classe', views.ClasseViewSet)
router.register(r'subclasse', views.SubclasseViewSet)
router.register(r'setor', views.SetorViewSet)
router.register(r'comercio', views.ComercioViewSet)
router.register(r'arrecadacao', views.ArrecadacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include(router.urls), name='api'),
]
