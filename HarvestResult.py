from datetime import datetime
import codecs
import csv
from collections import defaultdict
from LinearRegression import LinearRegression
import math

class HarvestResult:
    def result(self, predict, clima, tree, a, b1, b2, b3, b4):
        data_temp_chuva = self.calcular_medias_temp(clima)

        data = [linha[0] for linha in data_temp_chuva[0:]]
        preci = [linha[1] for linha in data_temp_chuva[0:]]
        temp = [linha[2] for linha in data_temp_chuva[0:]]

        x1 = sum(temp)/len(temp)
        x2 = sum(preci)/len(preci)
        x3 = self.ETo_n(predict, clima)
        x4 = tree        
        
        Y = a+(b1*x1)+(b2*x2)+(b3*x3)+(b4*x4)

        return Y, x1, x2, x3, x4
    
    def read_csv(self, clima):
        temp = []
        with codecs.open(clima, 'r', 'utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            for row in csvreader:
                data_hora = datetime.strptime(row[0], '%d/%m/%Y')
                chuva = float(row[1].replace(',', '.'))
                temperatura = float(row[2].replace(',', '.'))
                temp.append([data_hora, chuva, temperatura])
        
        return temp

    def calcular_medias_temp(self, clima):
            
            temp = self.read_csv(clima)
            # Dicionários para somar e contar os valores por mês
            soma_temperaturas = defaultdict(float)
            soma_chuvas = defaultdict(float)
            contagem = defaultdict(int)

            # Processar cada entrada dos dados
            for data_hora, temperatura, chuva in temp:
                mes_ano = data_hora.strftime('%m/%Y')
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
    
    def ETo_n(self, predict, clima):
        a_i_list = [0.49239,0.01793,-0.0000771,0.000000675]
        C = [0.070257, 0.000907,0.00148]
        D = [0.399912,0.006758,0.002697]
        C0 = 0.006918
        ETo_n = []
        media_anual = []
        ano_atual = None

        #lat = predict.lat()
        Tj_list = self.calcular_medias_temp(clima)
        dias = self.dias_ano(clima)
            
        for item in Tj_list:            
            # Extraindo o ano a partir da data
            data = datetime.strptime(item[0], '%m/%Y')
            temperatura = item[2]

            ano = data.year
            
            # Verifica se estamos no ano desejado
            if ano_atual is None:
                ano_atual = ano
            
            if ano_atual == ano:
                media_anual.append(temperatura)
            else:
                # Processa o ano completo que foi coletado
                I = 0.08745 * sum([temp ** 1.514 for temp in media_anual])
                
                a = sum(a_i * I**i for i, a_i in enumerate(a_i_list))

                an = []

                # Calculando os termos da soma
                for d in range(dias):
                    soma = sum(C * math.sin((2 * math.pi * d) / 365) - D * math.cos((2 * math.pi * d) / 365) for C, D in zip(C, D))
                    result = C0 + soma
                    an.append(result)

                phi_rad = math.radians(predict.lat_())
                Hn = []

                # Calculando Hn
                for alpha_n in an:
                    alpha_n_rad = math.radians(alpha_n)
                    Hn.append((24 / math.pi) * math.acos(-math.tan(alpha_n_rad) * math.tan(phi_rad)))

                Tn_m = sum(media_anual) / len(media_anual)
                Hn_m = sum(Hn) / len(Hn)

                ETo_n.append(0.53 * (10 * (Tn_m / I)) ** a * ((Hn_m / 12) * 30.41))

                # Limpa os dados para o próximo ano
                media_anual.clear()

                # Atualiza o ano atual
                ano_atual = ano

                # Adiciona a temperatura do novo ano
                media_anual.append(temperatura)

        # Processa os dados do último ano
        if media_anual:
            I = 0.08745 * sum([temp ** 1.514 for temp in media_anual])
            a = sum(a_i * I ** i for i, a_i in enumerate(a_i_list))

            dias = self.dias_ano(clima)
            an = []

            for d in range(dias):
                soma = sum(C * math.sin((2 * math.pi * d) / 365) - D * math.cos((2 * math.pi * d) / 365) for C, D in zip(C, D))
                result = C0 + soma
                an.append(result)

            phi_rad = math.radians(predict.lat_())
            Hn = []

            for alpha_n in an:
                alpha_n_rad = math.radians(alpha_n)
                Hn.append((24 / math.pi) * math.acos(-math.tan(alpha_n_rad) * math.tan(phi_rad)))

            Tn_m = sum(media_anual) / len(media_anual)
            Hn_m = sum(Hn) / len(Hn)

            ETo_n = (0.53 * (10 * (Tn_m / I)) ** a * ((Hn_m / 12) * dias))

        return ETo_n
    
    def dias_ano(self, clima):
        # Usar um conjunto para armazenar datas únicas
        dias_unicos = set()
        
        # Iterar sobre a lista de dados
        for linha in clima:
            # Dividir a linha pelo delimitador ';'
            data = linha.split(';')[0]
            # Adicionar a data ao conjunto
            dias_unicos.add(data)
        
        # Retornar o número de dias únicos
        return len(dias_unicos)