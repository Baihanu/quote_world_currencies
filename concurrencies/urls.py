"""concurrencies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import requests
from ninja import NinjaAPI


api = NinjaAPI()


@api.get("/cotacao")
def cotacao(request, de: str, para:str, quantia:float):
    """
    Função para pegar e fazer cotação das seguintes combinações de moedas
    USD-BRL,  USD-EUR,  BRL-USD,  BRL-EUR,  EUR-USD,  EUR-BRL,
    BTC-USD,  BTC-BRL,  BTC-EUR,  ETH-USD,  ETH-BRL,  ETH-EUR,
    """
    moeda = f'{de}-{para}'

    link = f'https://economia.awesomeapi.com.br/last/{moeda}'
    requisicao = requests.get(link)
    fk_result = requisicao.json()[f'{de}{para}']

    resultado = {
        'Compra': fk_result['bid'],
        'Venda': fk_result['ask'],
        'Ultima Atualizacao': fk_result['create_date'],
        'Minima': fk_result['low'],
        'Maxima': fk_result['high'],
        'Variacao': fk_result['varBid'],
        'Porcentagem de Variacao': fk_result['pctChange'],
        f'Valor em {de}': quantia,
        f'Valor em {para}': (quantia*float(fk_result['bid']))
    }

    return {f'Cotacao de {de} para {para}': resultado}

# TODO: Implementar funções para tratar calculos que a api não vai ter USD/BRL/EUR/ETH-BTC, USD/BRL/EUR/BTC-ETH 


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls)
]
