# Importando as bibliotecas Ultalytics para utilizar o YOLO v8.
from ultralytics import YOLO
from ultralytics.utils.downloads import GITHUB_ASSETS_STEMS
from datetime import datetime
from collections import defaultdict
import csv
import codecs
import os
from IPython.display import display, Image
from IPython import display
display.clear_output()

class Predict:
    # Inicializar a predição das imagens
    def __init__(self, pt, directory, lat, temp_dir, tree_fruit_dir):
        self.pt = pt
        self.directory = directory
        self.lat = lat
        self.temp_dir = temp_dir
        self.tree_fruit_dir = tree_fruit_dir

    # iniciar a predição dos objetos
    def image_predict(self):
        model = YOLO(self.pt)
        result = model.predict(self.directory, conf=0.1)

        data_fruit = [len(r.boxes) for r in result]

        return data_fruit
    
    def lat_(self):
        lat = self.lat
        return lat

    def temp_list(self):
        temp = []
        with codecs.open(self.temp_dir, 'r', 'utf') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            for row in csvreader:
                data_hora = datetime.strptime(row[0], '%d/%m/%Y')
                chuva = float(row[1].replace(',', '.'))
                temperatura = float(row[2].replace(',', '.'))
                temp.append([data_hora, chuva, temperatura])
        return temp
    
    def tree_list(self):
        tree = []
        with codecs.open(self.tree_fruit_dir, 'r', 'utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            for row in csvreader:
                ano = datetime.strptime(row[0], '%Y')
                arvore = float(row[1].replace(',', '.'))
                fruta = float(row[2].replace(',', '.'))
                tree.append([ano, arvore, fruta])
        return tree
    
    def calcular_medias_mensais_temp(self):
        temp = self.temp_list()
        # Dicionários para somar e contar os valores por mês
        soma_temperaturas = defaultdict(float)
        soma_chuvas = defaultdict(float)
        contagem = defaultdict(int)

        # Processar cada entrada dos dados
        for data_hora, temperatura, chuva in temp:
            mes_ano = data_hora.strftime('%Y-%m')
            soma_temperaturas[mes_ano] += temperatura
            soma_chuvas[mes_ano] += chuva
            contagem[mes_ano] += 1

        # Calcular médias
        medias_mensais = []
        for mes_ano in soma_temperaturas:
            media_temp = soma_temperaturas[mes_ano] / contagem[mes_ano]
            media_chuva = soma_chuvas[mes_ano] / contagem[mes_ano]
            medias_mensais.append([mes_ano, media_temp, media_chuva])

        return medias_mensais
    
    def calcular_medias_mensais_tree(self):
        temp = self.tree_list()
        # Dicionários para somar e contar os valores por mês
        soma_temperaturas = defaultdict(float)
        soma_chuvas = defaultdict(float)
        contagem = defaultdict(int)

        # Processar cada entrada dos dados
        for data_hora, temperatura, chuva in temp:
            mes_ano = data_hora.strftime('%Y-%m')
            soma_temperaturas[mes_ano] += temperatura
            soma_chuvas[mes_ano] += chuva
            contagem[mes_ano] += 1

        # Calcular médias
        medias_mensais = []
        for mes_ano in soma_temperaturas:
            media_temp = soma_temperaturas[mes_ano] / contagem[mes_ano]
            media_chuva = soma_chuvas[mes_ano] / contagem[mes_ano]
            medias_mensais.append([mes_ano, media_temp, media_chuva])

        return medias_mensais
    
    def calcular_medias_anuais(self):
        temp = self.temp_list()
        # Dicionários para somar e contar os valores por mês
        soma_temperaturas = defaultdict(float)
        soma_chuvas = defaultdict(float)
        contagem = defaultdict(int)

        # Processar cada entrada dos dados
        for data_hora, temperatura, chuva in temp:
            ano = data_hora.strftime('%Y')
            soma_temperaturas[ano] += temperatura
            soma_chuvas[ano] += chuva
            contagem[ano] += 1

        # Calcular médias
        medias_anuais = []
        for ano in soma_temperaturas:
            media_temp = soma_temperaturas[ano] / contagem[ano]
            media_chuva = soma_chuvas[ano] / contagem[ano]
            medias_anuais.append([ano, media_temp, media_chuva])

        return medias_anuais
    
    def dias_ano(self):
        fila = []

        for i in range(1, 366):
            fila.append(i)
        
        return fila
    
    def all_data_list(self):
        data_temp_chuva = self.calcular_medias_anuais()
        arvore_fruta = self.calcular_medias_mensais_tree()

        data = [linha[0] for linha in data_temp_chuva[0:]]
        temp = [linha[1] for linha in data_temp_chuva[0:]]
        preci = [linha[2] for linha in data_temp_chuva[0:]]
        tree = [linha[1] for linha in arvore_fruta[0:]]
        fruit = [linha[2] for linha in arvore_fruta[0:]]

        return data, temp, preci, tree, fruit