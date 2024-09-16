import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import mplcyberpunk
import yfinance as yf
from cache import obter_dados_bancarios 

def toYahooFinance(ativo):
    return ativo if ativo == "^BVSP" else ativo + ".SA" 

# Definindo os parâmetros
start = "2010-01-01"
end = "2022-04-30"
lista_de_ativos = ["ITUB4", "BBAS3", "SANB4", "BBDC4", "^BVSP"]
tickers = list(map(toYahooFinance, lista_de_ativos))
print(tickers)

lucro_bancos = pd.read_excel('lucro_bancos_2010_2022.xlsx')
lucro_bancos["data"] = pd.to_datetime(lucro_bancos["data"])
lucro_bancos.set_index("data", inplace=True)
lucro_bancos_2015 = lucro_bancos[lucro_bancos.index >= "2015-01-01"]
print(lucro_bancos)

# Obtendo os dados (usando cache se disponível)
dados_bancario = obter_dados_bancarios(tickers, start, end)

# dados_bancario = yf.download(tickers, start = "2010-01-01", end = "2022-04-30")
# dados_bancario = dados_bancario["Adj Close"]
print(dados_bancario)

dataframe_colunas_selecionadas = dados_bancario[["BBAS3.SA", "ITUB4.SA"]]
dados_2015 = dados_bancario[dados_bancario.index >= "2015-01-01"]
cotacao_maior_que_15 = dados_bancario[dados_bancario["ITUB4.SA"] > 15]

itau = dados_bancario["ITUB4.SA"]
bradesco = dados_bancario["BBDC4.SA"]
santander = dados_bancario["SANB4.SA"]
banco_do_brasil = dados_bancario["BBAS3.SA"]
ibov = dados_bancario["^BVSP"]

def retorno(lista_cotacoes):
    retorno = lista_cotacoes[-1] / lista_cotacoes[0] - 1

    return round(retorno * 100, 2)

retorno_itau = retorno(itau)
retorno_bradesco = retorno(bradesco)
retorno_santander = retorno(santander)
retorno_banco_do_brasil = retorno(banco_do_brasil)
retorno_ibov = retorno(ibov)

print(itau)

df_retornos = pd.DataFrame(
    data = {"retornos" : [retorno_itau, retorno_bradesco, retorno_banco_do_brasil, retorno_santander, retorno_ibov]},
    index = ["Itau", "Bradesco", "Banco do Brasil", "Santander", "Ibovespa"]
)

df_retornos["retornos"] = df_retornos["retornos"] * 100
df_retornos = df_retornos.sort_values(by = "retornos", ascending = False)

print(df_retornos)

plt.style.use("cyberpunk")
fig, ax = plt.subplots()

ax.set_title("Retornos dos Bancos")
ax.bar(df_retornos.index, df_retornos["retornos"])
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(fontsize = 9)
plt.show()

var_lucro_bancos = lucro_bancos.iloc[-1] / lucro_bancos.iloc[0] - 1
var_lucro_bancos = var_lucro_bancos.sort_values(ascending = False)
print(var_lucro_bancos)

fig, ax = plt.subplots()

ax.set_title("Lucros dos Bancos")
ax.bar(var_lucro_bancos.index, var_lucro_bancos.values)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(fontsize = 9)
plt.show()

def resample_periodo(dado, periodo):
    dado_periodo_novo = dado.resample(f"{periodo}").last()
    dado_periodo_novo = dado_periodo_novo.pct_change()
    dado_periodo_novo = dado_periodo_novo.dropna()

    return dado_periodo_novo

itau_ano_a_ano = resample_periodo(itau, "Y")
print(itau_ano_a_ano)

# Mudando cotação dia a dia para anual
print(itau.resample("YE").last())

ibov_ano_a_ano = resample_periodo(ibov, "Y")

itau_menos_ibov = itau_ano_a_ano - ibov_ano_a_ano
print(itau_menos_ibov)

itau_menos_ibov.plot()
plt.show()

def long_short(long, short, periodo):
    var_long = resample_periodo(long, periodo)
    var_short = resample_periodo(short, periodo)
    outperform = var_long - var_short
    print(outperform)

    plt.plot(outperform)
    plt.show()

long_short(itau, banco_do_brasil, "Y")

print("Fim")
