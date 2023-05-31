import talib as ta
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import pandas_ta as pta
import gc
from stock_list import stocks

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

# DOWNLOAD DADOS PARA CRIAR O DATAFRAME
index = 0
while index < len(stocks):
    element = stocks[index]

    preco = yf.download(tickers = element, period = '6mo', interval = '1d')

    # SOLICITAR OS DADOS DO INDICADOR ADX PELO PANDAS_TA
    adx = pta.adx(preco['High'], preco['Low'], preco['Close'])

    #CONCATENAR OS DADOS DO DATAFRAME 'ADX' AO DATAFRAME PRECOS
    preco = pd.concat([preco , adx], axis = 1)

    #SOLICITAR OS DADOS DO INDICADOR BANDAS DE BOLLINGER PELO PANDAS_TA
    bol = pta.bbands(preco['Close'])

    #CONCATENAR OS DATAFRAMES BOL E PRECOS
    preco = pd.concat([preco , bol], axis = 1)

    #RENOMEAR AS COLUNAS PARA O PADRÃO USADO ATÉ AQUI
    preco = preco.rename(columns = {'BBL_5_2.0' : 'BB_Lower'})
    preco = preco.rename(columns = {'BBM_5_2.0' : 'BB_Medium'})
    preco = preco.rename(columns = {'BBU_5_2.0' : 'BB_Upper'})

    #DEPOIS DE CONCATENADO AO DATAFRAME PRINCIPAL, DROPAR OS DATAFRAMES ADX e BOL PARA LIMPAR
    #A MEMORIA
    lst = [adx]
    del adx
    del lst

    lst = [bol]
    del bol
    del lst

    # CALCULAR DIDI INDEX
    preco['Didi_3'] = ta.MA(preco['Close'],3)
    preco['Didi_8'] = ta.MA(preco['Close'],8)
    preco['Didi_20'] = ta.MA(preco['Close'],20)
    preco['Didi_Rapida'] = preco['Didi_3'] - preco['Didi_8']
    preco['Didi_Lenta'] = preco['Didi_20'] - preco['Didi_8']

    # DROPAR AS COLUNAS DESNECESSÁRIAS
    preco = preco.drop(columns = ['Volume', 'BBB_5_2.0', 'BBP_5_2.0'])

    # PEGAR SÓ OS ÚLTIMOS 60 DIAS DO DATAFRAME PARA FAZER O PLOT
    preco = preco.iloc[-60:]

    #CONDIÇÕES PARA O ARQUIVO SER PLOTADO OU NÃO
    if (preco.iloc[-1]['Didi_Rapida']) > (preco.iloc[-2]['Didi_Rapida']) and \
        (preco.iloc[-1]['Didi_Lenta']) < (preco.iloc[-2]['Didi_Lenta']) and \
        (preco.iloc[-1]['Didi_Rapida']) >= -5 and (preco.iloc[-1]['Didi_Rapida']) <= 5 and \
        (preco.iloc[-1]['Didi_Lenta']) <= 5 and (preco.iloc[-1]['Didi_Lenta']) >= -5 :
                
        #PLOTAGEM DA LINHA SUPERIOR: PRECO DE FECHAMENTO COM BANDAS DE BOLLINGER
        plt.subplot(3,1,1)
        plt.title(('' + element + ' Preço (60 dias)'))
        plt.plot(preco['BB_Medium'], '-.', linewidth = 0.75)
        plt.plot(preco['Close'], color='black', linewidth = 1)
        plt.fill_between(
            preco['BB_Medium'].index,
            preco['BB_Upper'], preco['BB_Lower'],
            alpha= .1,
            color = 'red'
            )
        #PLOTAGEM DA LINHA CENTRAL: DIDI INDEX
        plt.subplot(3,1,2)
        plt.title('Dd INDX')
        plt.axhline(y = 0, color = 'black', linestyle = '--', linewidth = 0.8)
        plt.plot(preco['Didi_Rapida'], color = 'green', linewidth = 1)
        plt.plot(preco['Didi_Lenta'], color ='red', linewidth = 1)
        #PLOTAGEM DA LINHA INFERIOR: ADX COM DMP E DMN
        plt.subplot(3,1,3)
        plt.title('ADX + DMI')
        plt.axhline(y = 25, color = 'black', linestyle = '--', linewidth = 0.8)
        plt.plot(preco['ADX_14'], '-.')
        plt.plot(preco['DMP_14'], color='green', linewidth = 1)
        plt.plot(preco['DMN_14'], color = 'red', linewidth = 1)
    
        #EXPORTAR O GRÁFICO
        destino = 'C:/Users/Casa/Desktop/indicadores/proximos/'
        plt.savefig(destino + '' + element)
        lst = preco
        del preco
        del lst
        gc.collect()
        plt.close("all")
        index += 1
        
    else:
        lst = preco
        del preco
        del lst
        gc.collect()
        plt.close("all")
        index += 1

print("Processo terminado.")