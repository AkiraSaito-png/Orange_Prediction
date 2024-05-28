from Predict import Predict
from LinearRegression import LinearRegression
from GraficPlot import GraficPlot
from HarvestResult import HarvestResult
import os

directory = "C:/Users/akira/OneDrive/Orange_Prediction/project/Laranja-1/test/images"
pt = "C:/Users/akira/OneDrive/Orange_Prediction/project/runs/detect/train/weights/best.pt"
temp_dir = 'C:/Users/akira/OneDrive/Orange_Prediction/project/data/meteorologia-20152023.csv'
tree_fruit_dir = 'C:/Users/akira/OneDrive/Orange_Prediction/project/data/safra-20152023.csv'

#------------------------------------------///-----------------------------------------------

lat = -20.94916666
clima = 'C:/Users/akira/OneDrive/Orange_Prediction/project/data/generatedBy_react-csv.csv'
tree = 38932


predict = Predict(pt, directory, lat, temp_dir, tree_fruit_dir)
lr = LinearRegression()
gp = GraficPlot()
hr = HarvestResult()

ip = predict.image_predict()
os.system('cls')
print(f'\n\n{"RELATÓRIO DE COLETA DE DADOS POR IMAGENS":^60}')
print('-' * 70)
print("N°" + 'DE PÉS DE LARANJAS' + ' '*19 + "N°" + 'DE LARANJAS')
print('-' * 70)
print(f"{len(ip)}" + ' '*37 + f"{sum(ip)}\n\n\n")
gp.temp_graph(predict)
gp.fruit_graph(predict)
a, b1, b2, b3, b4 = lr.predict_train(predict)
hr.result(predict, clima, tree,a, b1, b2, b3, b4)