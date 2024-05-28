import math
from datetime import datetime

class LinearRegression:
    def predict_train(self, predict):
        
        # Desbilitado, por não atendenr o numero de dados suficientes
        ##fruit, age = predict.image_predict()
        year, preci, temp, tree, fruit = predict.all_data_list()
        evapo = self.pessipitationtemperature(predict)

        n = len(fruit)

        # Inicializar somatórias
        sum_y = sum(fruit)
        sum_x1 = sum(temp)
        sum_x2 = sum(preci)
        sum_x3 = sum(evapo)
        sum_x4 = sum(tree)

        med_y = sum_y/len(fruit)
        med_x1 = sum_x1/len(temp)
        med_x2 = sum_x2/len(preci)
        med_x3 = sum_x3/len(evapo)
        med_x4 = sum_x4/len(tree)

        sum_x1_y = sum(x1 * y for x1, y in zip(temp, fruit))
        sum_x2_y = sum(x2 * y for x2, y in zip(preci, fruit))
        sum_x3_y = sum(x3 * y for x3, y in zip(evapo, fruit))
        sum_x4_y = sum(x4 * y for x4, y in zip(tree, fruit))

        sum_x1_x1 = sum(x1 * x1 for x1 in temp)
        sum_x2_x2 = sum(x2 * x2 for x2 in preci)
        sum_x3_x3 = sum(x3 * x3 for x3 in evapo)
        sum_x4_x4 = sum(x4 * x4 for x4 in tree)

        sum_x1_x2 = sum(x1 * x2 for x1, x2 in zip(temp, preci))
        sum_x1_x3 = sum(x1 * x3 for x1, x3 in zip(temp, evapo))
        sum_x1_x4 = sum(x1 * x4 for x1, x4 in zip(temp, tree))
        sum_x2_x3 = sum(x2 * x3 for x2, x3 in zip(preci, evapo))
        sum_x2_x4 = sum(x2 * x4 for x2, x4 in zip(preci, tree))
        sum_x3_x4 = sum(x3 * x4 for x3, x4 in zip(evapo, tree))

        # Montar sistema de equações
        A = [
            [n, sum_x1, sum_x2, sum_x3, sum_x4],
            [sum_x1, sum_x1_x1, sum_x1_x2, sum_x1_x3, sum_x1_x4],
            [sum_x2, sum_x1_x2, sum_x2_x2, sum_x2_x3, sum_x2_x4],
            [sum_x3, sum_x1_x3, sum_x2_x3, sum_x3_x3, sum_x3_x4],
            [sum_x4, sum_x1_x4, sum_x2_x4, sum_x3_x4, sum_x4_x4]
        ]

        B = [sum_y, sum_x1_y, sum_x2_y, sum_x3_y, sum_x4_y]

        # Resolver sistema de equações usando eliminação de Gauss
        def gauss_jordan(A, B):
            n = len(B)
            M = [row[:] for row in A]  # Fazer uma cópia de A

            for i in range(n):
                M[i].append(B[i])

            for i in range(n):
                # Pivotização
                max_el = abs(M[i][i])
                max_row = i
                for k in range(i + 1, n):
                    if abs(M[k][i]) > max_el:
                        max_el = abs(M[k][i])
                        max_row = k

                # Trocar linhas
                M[max_row], M[i] = M[i], M[max_row]

                # Tornar os elementos abaixo deste pivô todos zeros na coluna atual
                for k in range(i + 1, n):
                    c = -M[k][i] / M[i][i]
                    for j in range(i, n + 1):
                        if i == j:
                            M[k][j] = 0
                        else:
                            M[k][j] += c * M[i][j]

            # Resolver sistema de equações Ax = B para uma matriz triangular superior
            X = [0 for i in range(n)]
            for i in range(n - 1, -1, -1):
                X[i] = M[i][n] / M[i][i]
                for k in range(i - 1, -1, -1):
                    M[k][n] -= M[k][i] * X[i]

            return X

        alfa, beta_1, beta_2, beta_3, beta_4 = gauss_jordan(A, B)
        
        safra_y = [alfa + beta_1*x1 + beta_2*x2 + beta_3*x3 + beta_4*x4 for x1, x2, x3, x4 in zip(temp, preci, evapo, tree)]

        SS_total = sum((y - med_y)**2 for y in fruit)
        SS_residual = sum((y - y_pred)**2 for y, y_pred in zip(fruit, safra_y))
        R_squared = 1 - (SS_residual / SS_total)

        print(f"O modelo treinado tem uma confiabilidade de: {R_squared:.2%}")

        return alfa, beta_1, beta_2, beta_3, beta_4


    def pessipitationtemperature(self, predict):
        a_i_list = [0.49239,0.01793,-0.0000771,0.000000675]
        C = [0.070257, 0.000907,0.00148]
        D = [0.399912,0.006758,0.002697]
        C0 = 0.006918
        ETo_n = []
        media_anual = []
        ano_atual = None

        #lat = predict.lat()
        Tj_list = predict.calcular_medias_mensais_temp()
            
        for item in Tj_list:            
            # Extraindo o ano a partir da data
            data = datetime.strptime(item[0], '%Y-%m')
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

                dias = predict.dias_ano()
                an = []

                # Calculando os termos da soma
                for d in dias:
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

            dias = predict.dias_ano()
            an = []

            for d in dias:
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

            ETo_n.append(0.53 * (10 * (Tn_m / I)) ** a * ((Hn_m / 12) * 30.41))

        return ETo_n
    
    def R2(self, Y, age, med_age):
        u = []
        u2 = []
        YY2 = []
        
        # soma dos quadrados
        for y, a in zip(age, Y):
            u.append(y-a) 

        # soma dos quadrados da regressão 
        for y in Y:
            YY2.append((y-med_age)**2) 

        # soma dos quadrados dos resíduos 
        for y in u:
            u2.append(y**2)

        R2 = sum(YY2)/(sum(YY2)+sum(u2))
        return R2*100