from rest_framework import serializers
from .              import models

class SecaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Secao
        fields = '__all__'

class DivisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Divisao
        fields = '__all__'
        
class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grupo
        fields = '__all__'
        
class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Classe
        fields = '__all__'
        
class SubclasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subclasse
        fields = '__all__'
        
class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Setor
        fields = '__all__'
        
class ComercioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comercio
        fields = '__all__'
        
class ArrecadacaoSerializer(serializers.ModelSerializer):
    secao = serializers.CharField(source='subclasse.classe.grupo.divisao.secao.codigo')
    divisao = serializers.CharField(source='subclasse.classe.grupo.divisao.codigo')
    grupo = serializers.CharField(source='subclasse.classe.grupo.codigo')
    classe = serializers.CharField(source='subclasse.classe.codigo')
    subclasse = serializers.CharField(source='subclasse.codigo')
    setor = serializers.CharField(source='setor.descricao')
    comercio = serializers.CharField(source='comercio.descricao')
    
    class Meta:
        model = models.Arrecadacao
        fields = ['id', 'valor', 'data', 'secao', 'divisao', 'grupo', 'classe', 'subclasse', 'setor', 'comercio']
