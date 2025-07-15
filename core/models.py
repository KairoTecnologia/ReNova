from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User

class Curriculo(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    resumo = models.TextField(blank=True, null=True, verbose_name="Resumo")
    habilidades = models.TextField(blank=True, null=True, verbose_name="Habilidades")
    experiencia = models.TextField(blank=True, null=True, verbose_name="Experiência")
    educacao = models.TextField(blank=True, null=True, verbose_name="Educação")
    ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última atualização")

    def __str__(self):
        return f"Currículo de {self.usuario.username}"

    class Meta:
        verbose_name = "Currículo"
        verbose_name_plural = "Currículos"

class CursoRecomendado(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    link = models.URLField(blank=True, null=True, verbose_name="Link")
    area = models.CharField(max_length=255, verbose_name="Área")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Curso recomendado"
        verbose_name_plural = "Cursos recomendados"

class Empresa(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=50, verbose_name="Estado")
    latitude = models.FloatField(blank=True, null=True, verbose_name="Latitude")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Longitude")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

class Vaga(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa")
    titulo = models.CharField(max_length=255, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    requisitos = models.TextField(blank=True, null=True, verbose_name="Requisitos")
    link_aplicacao = models.URLField(blank=True, null=True, verbose_name="Link para candidatura")
    data_publicacao = models.DateField(auto_now_add=True, verbose_name="Data de publicação")

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nome}"

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"
=======

# Create your models here.
>>>>>>> 6f95e80db7c9f4ebd994d9de55fb275495d12e3f
