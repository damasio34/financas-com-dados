import os
import joblib
import yfinance as yf

# Função para carregar ou baixar os dados
def obter_dados_bancarios(tickers, start, end, cache_file='dados_bancario_cache.pkl'):
    if os.path.exists(cache_file):
        print("Carregando dados do cache...")
        return joblib.load(cache_file)
    else:
        print("Baixando dados do Yahoo Finance...")
        dados_bancario = yf.download(tickers, start=start, end=end)
        dados_bancario = dados_bancario["Adj Close"]
        joblib.dump(dados_bancario, cache_file)
        return dados_bancario
