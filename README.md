# R-CNN
## Introdução
O Region-based Convolutional Neural Network (R-CNN) é uma técnica pioneira na área de visão computacional e detecção de objetos em imagens. Introduzido por Ross Girshick e colaboradores em 2014, o R-CNN revolucionou a abordagem para a detecção de objetos ao combinar as capacidades de redes neurais convolucionais (CNNs) com métodos de seleção de regiões. Essa abordagem não apenas melhorou significativamente a precisão da detecção de objetos, mas também estabeleceu uma base para o desenvolvimento de técnicas mais avançadas, como o Fast R-CNN e o Faster R-CNN. Neste texto, exploraremos os princípios fundamentais do R-CNN, seu funcionamento básico e como ele contribuiu para avanços subsequentes na detecção de objetos em imagens.
## Funcionamento
O R-CNN (Region-based Convolutional Neural Network) é um algoritmo utilizado para detecção de objetos em imagens. Ele opera em várias etapas:

1. Proposição de Regiões: O primeiro passo é gerar uma grande quantidade de regiões candidatas que possam conter objetos. Isso pode ser feito usando técnicas como o algoritmo de propagação de regiões seletivas (Selective Search), que identifica regiões promissoras na imagem com base em critérios como cor, textura, tamanho e forma.
2. Extração de Características: Para cada região proposta, uma subimagem é recortada da imagem original e redimensionada para uma dimensão fixa. Em seguida, é aplicada uma rede neural convolucional (CNN) pre-treinada para extrair características da subimagem. Essas características são representações de baixo nível, como bordas e texturas, bem como características de alto nível, como formas e padrões.
3. Classificação de Regiões: As características extraídas de cada região proposta são alimentadas em um classificador, que determina a probabilidade de a região conter um objeto de uma classe específica. Tipicamente, um classificador baseado em máquina de vetores de suporte (SVM) é treinado para classificar as regiões em categorias como "objeto" ou "não objeto" para cada classe de interesse.
4. Refinamento de Caixas Delimitadoras: Após a classificação, as regiões que foram identificadas como contendo objetos são refinadas ajustando suas caixas delimitadoras para melhor se ajustarem aos contornos dos objetos. Isso é feito por meio de uma etapa de regressão, que otimiza as coordenadas das caixas delimitadoras com base nas características da região proposta.
5. Supressão Não-Máxima: Para evitar a duplicação de detecções, uma etapa final de supressão não-máxima é aplicada. Isso envolve a remoção de detecções redundantes que têm uma sobreposição significativa com detecções mais confiantes.

O R-CNN é uma abordagem eficaz para detecção de objetos, mas é relativamente lento devido à necessidade de processar cada região proposta separadamente. No entanto, sua precisão e capacidade de detecção detalhada tornaram-no uma base importante para o desenvolvimento de técnicas mais rápidas e eficientes, como o Fast R-CNN e o Faster R-CNN.

![Fig02-2](https://github.com/AkiraSaito-png/Orange_detection_R-CNN/assets/65370577/23a0c7a5-3f01-4513-b245-c45516cd26dd)

R-CNN resolve o problema das múltiplas saídas usando uma Busca Seletiva da seguinte forma:

1. Gerar subsegmentação inicial: geramos muitas regiões candidatas.
2. Usar algoritmo guloso para combinar recursivamente regiões semelhantes em regiões maiores.
3. Utilizar as regiões geradas para produzir as propostas finais de região candidata.

R-CNN gera inicialmente em torno de 2000 candidatos usando o algoritmo acima, que é baseado em técnicas simples de visão computacional tradicional. A partir daí:

1. Cada candidato é reformatado para uma imagem quadrada de tamanho padrão;
2. Imagem é alimentada a uma rede neural que gera vetores de características de 4096 dimensões como saída;
3. Uma SVM classifica o vetor de características produzindo duas saídas:
   - uma classificação
   - uma indicação de desvio (offset) que pode ser usada para ajustar o bounding box.

![images](https://github.com/AkiraSaito-png/Orange_detection_R-CNN/assets/65370577/fa9881b4-9edf-4f12-bd7a-2aa75a7be537)

Desvantagens do modelo:

1. Lento para treinar: o treino é em dois estágios;
2. Lentíssimo para executar: para cada imagem a R-CNN primeiramente classifica 2000 subimagens.
