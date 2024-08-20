from django.db import models

class Secao(models.Model):
    codigo = models.CharField(max_length=1, unique=True, blank=False)
    descricao = models.CharField(max_length=255, unique=True, blank=False)
    
    def __str__(self) -> str:
        return str(self.codigo)
    
class Divisao(models.Model):
    codigo = models.CharField(max_length=2, unique=True, blank=False)
    descricao = models.CharField(max_length=255, unique=True, blank=False)
    secao = models.ForeignKey(Secao, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return str(self.codigo)
    
class Grupo(models.Model):
    codigo = models.CharField(max_length=3, unique=True, blank=False)
    descricao = models.CharField(max_length=255, unique=True, blank=False)
    divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return str(self.codigo)
    
class Classe(models.Model):
    codigo = models.CharField(max_length=5, unique=True, blank=False)
    descricao = models.CharField(max_length=255, unique=True, blank=False)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return str(self.codigo)
    
class Subclasse(models.Model):
    codigo = models.CharField(max_length=7, unique=True, blank=False)
    descricao = models.CharField(max_length=255, unique=True, blank=False)
    classe = models.ForeignKey(Classe, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return str(self.codigo)
    
class Setor(models.Model):
    descricao = models.CharField(max_length=255, unique=True, blank=False)
    
    def __str__(self) -> str:
        return str(self.descricao)
    
class Comercio(models.Model):
    descricao = models.CharField(max_length=255, unique=True, blank=False)
    
    def __str__(self) -> str:
        return str(self.descricao)
    
class Arrecadacao(models.Model):
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    subclasse = models.ForeignKey(Subclasse, on_delete=models.PROTECT)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    comercio = models.ForeignKey(Comercio, on_delete=models.PROTECT)
    data = models.DateField()
    
    def __str__(self) -> str:
        return str(self.id)