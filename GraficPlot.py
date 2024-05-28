import matplotlib.pyplot as plt
from Predict import Predict

class GraficPlot:
    def temp_graph(self, predict):
        
        dados_lista = predict.calcular_medias_anuais()

        datas = [linha[0] for linha in dados_lista[0:]]
        chuvas = [linha[1] for linha in dados_lista[0:]]
        temperaturas = [linha[2] for linha in dados_lista[0:]]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))

        # Plotar o gráfico de temperaturas
        ax1.plot(datas, temperaturas)
        ax1.set_title('Média mensal de temperatura (2015 - 2023)')
        ax1.set_xlabel('Ano')
        ax1.set_ylabel('Temperatura (C)')
        ax1.tick_params(axis='x', rotation=45)

        # Plotar o gráfico de chuvas
        ax2.plot(datas, chuvas)
        ax2.set_title('Média mensal de precipitação (2015 - 2023)')
        ax2.set_xlabel('Ano')
        ax2.set_ylabel('Chuva (mm)')
        ax2.tick_params(axis='x', rotation=45)

        # Ajusta o layout para evitar sobreposição de rótulos
        plt.tight_layout()

        # Mostra o gráfico
        plt.show()

    def fruit_graph(self, predict):
        dados_lista = predict.tree_list()

        ano = [linha[0] for linha in dados_lista]
        tree = [linha[1] for linha in dados_lista]
        fruit = [linha[2] for linha in dados_lista]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))

        # Plotar o gráfico de temperaturas
        ax1.plot(ano, tree)
        ax1.set_title('Números de plantas produtivas (2015 - 2023)')
        ax1.set_xlabel('Ano')
        ax1.set_ylabel('Plantas produtivas')

        # Plotar o gráfico de chuvas
        ax2.plot(ano, fruit)
        ax2.set_title('Resultado da safra (2015 - 2023)')
        ax2.set_xlabel('Ano')
        ax2.set_ylabel('Laranjas colhidas')

        # Ajusta o layout para evitar sobreposição de rótulos
        plt.tight_layout()

        # Mostra o gráfico
        plt.show()

    def evapo_graph(self, predict):
        dados_lista = predict.pessipitationtemperature()

        ano = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

        evapo = [linha[0] for linha in dados_lista[0:]]

        fig, (ax1) = plt.subplots(2, 1, figsize=(9, 7))

        # Plotar o gráfico de temperaturas
        ax1.bar(ano, evapo)
        ax1.set_title('Números de plantas produtivas (2015 - 2023)')
        ax1.set_xlabel('Ano')
        ax1.set_ylabel('Plantas produtivas')
        ax1.tick_params(axis='x', rotation=45)

        # Ajusta o layout para evitar sobreposição de rótulos
        plt.tight_layout()

        # Mostra o gráfico
        plt.show()