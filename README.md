# Rastreador
Script em Python para rastrear tendências de preços de ativos do mercado financeiro americano e gerar gráficos dos preços que estejam
dentro dos parâmetros configurados, facilitando o processo de rastreamento e auxiliando na tomada de decisão.

Este rastreador utiliza funções das bibliotecas Yahoo Finance, Talib, Pandas e MatplotLib para calcular os preços de fechamento diários
das 1550 ações com maior valor de mercado das bolsas americanas. São calculadas as médias móveis de 3, 8 e 20 períodos para a montagem
do indicador técnico Didi Index. Também são calculados o Diretional Moviment Index e as Bandas de Bollinger.
De acordo com os parâmetros do script quando os três indicadores convergem para indicação de entrada em uma determinada ação, seja compra,
seja venda, o script plotará o gráfico desta ação para que o usuário examine e realize a tomada de decisão de investimento.
