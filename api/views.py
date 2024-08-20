from django.shortcuts              import render
from rest_framework                import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .                             import models
from .                             import serializers
from .                             import filters

class SecaoViewSet(viewsets.ModelViewSet):
    queryset = models.Secao.objects.all()
    serializer_class = serializers.SecaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.SecaoFilter
    
class DivisaoViewSet(viewsets.ModelViewSet):
    queryset = models.Divisao.objects.all()
    serializer_class = serializers.DivisaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.DivisaoFilter
    
class GrupoViewSet(viewsets.ModelViewSet):
    queryset = models.Grupo.objects.all()
    serializer_class = serializers.GrupoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.GrupoFilter
    
class ClasseViewSet(viewsets.ModelViewSet):
    queryset = models.Classe.objects.all()
    serializer_class = serializers.ClasseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ClasseFilter
    
class SubclasseViewSet(viewsets.ModelViewSet):
    queryset = models.Subclasse.objects.all()
    serializer_class = serializers.SubclasseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.SubclasseFilter
    
class SetorViewSet(viewsets.ModelViewSet):
    queryset = models.Setor.objects.all()
    serializer_class = serializers.SetorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.SetorFilter
    
class ComercioViewSet(viewsets.ModelViewSet):
    queryset = models.Comercio.objects.all()
    serializer_class = serializers.ComercioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ComercioFilter
    
class ArrecadacaoViewSet(viewsets.ModelViewSet):
    queryset = models.Arrecadacao.objects.select_related(
        'subclasse__classe__grupo__divisao__secao',
        'setor',
        'comercio'
    ).all()
    serializer_class = serializers.ArrecadacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ArrecadacaoFilter