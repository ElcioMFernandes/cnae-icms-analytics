import django_filters
from . import models

class SecaoFilter(django_filters.FilterSet):
    class Meta:
        model = models.Secao
        fields = '__all__'
        
class DivisaoFilter(django_filters.FilterSet):
    class Meta:
        model = models.Divisao
        fields = '__all__'
        
class GrupoFilter(django_filters.FilterSet):
    class Meta:
        model = models.Grupo
        fields = '__all__'
        
class ClasseFilter(django_filters.FilterSet):
    class Meta:
        model = models.Classe
        fields = '__all__'
        
class SubclasseFilter(django_filters.FilterSet):
    class Meta:
        model = models.Subclasse
        fields = '__all__'

class SetorFilter(django_filters.FilterSet):
    class Meta:
        model = models.Setor
        fields = '__all__'

class ComercioFilter(django_filters.FilterSet):
    class Meta:
        model = models.Comercio
        fields = '__all__'
        
class ArrecadacaoFilter(django_filters.FilterSet):
    class Meta:
        model = models.Arrecadacao
        fields = '__all__'
