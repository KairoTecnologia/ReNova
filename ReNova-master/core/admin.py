from django.contrib import admin
from django.utils.html import format_html
from .models import Curriculo, CursoRecomendado, Empresa, Vaga

admin.site.site_header = format_html('<img src="/static/core/LogoReNova.png" style="height:80px; width:auto;">')
admin.site.site_title = "ReNova Admin"
admin.site.index_title = "Painel Administrativo ReNova"

admin.site.register(Curriculo)
admin.site.register(CursoRecomendado)
admin.site.register(Empresa)
admin.site.register(Vaga)

