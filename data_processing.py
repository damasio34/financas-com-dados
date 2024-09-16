import pandas as pd

# Adapta o ticker para o formato aceito pelo Yahoo Finance
def formata_ticker(ticker):
    return ticker if ticker == "^BVSP" else f"{ticker}.SA"

# Carrega os dados de lucro dos bancos a partir do arquivo Excel
def carregar_lucro_bancos(arquivo_excel):
    lucro_bancos = pd.read_excel(arquivo_excel)
    lucro_bancos["data"] = pd.to_datetime(lucro_bancos["data"])
    return lucro_bancos.set_index("data")

# Reamostra os dados de acordo com o período especificado
def reamostrar_por_periodo(dados, periodo):
    dados_resampled = dados.resample(periodo).last().pct_change().dropna()
    return dados_resampled
