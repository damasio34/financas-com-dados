import pandas as pd
import matplotlib.pyplot as plt
from cache import obter_dados_bancarios
from data_processing import formata_ticker, carregar_lucro_bancos, reamostrar_por_periodo
from finance_analysis import calcular_retorno, calcular_long_short
from plotting import plotar_grafico_retorno, plotar_long_short

# Definindo parâmetros globais
inicio = "2010-01-01"
fim = "2022-04-30"
lista_ativos = ["ITUB4", "BBAS3", "SANB4", "BBDC4", "^BVSP"]
tickers = list(map(formata_ticker, lista_ativos))

# Carrega lucro dos bancos e filtra a partir de 2015
lucro_bancos = carregar_lucro_bancos('lucro_bancos_2010_2022.xlsx')
lucro_bancos_2015 = lucro_bancos[lucro_bancos.index >= "2015-01-01"]

# Obtém dados bancários utilizando cache
dados_bancario = obter_dados_bancarios(tickers, inicio, fim)

# Seleciona as cotações de bancos específicos
itau = dados_bancario["ITUB4.SA"]
bradesco = dados_bancario["BBDC4.SA"]
santander = dados_bancario["SANB4.SA"]
banco_brasil = dados_bancario["BBAS3.SA"]
ibov = dados_bancario["^BVSP"]

# Calcula os retornos dos ativos
retornos = {
    "Itau": calcular_retorno(itau),
    "Bradesco": calcular_retorno(bradesco),
    "Banco do Brasil": calcular_retorno(banco_brasil),
    "Santander": calcular_retorno(santander),
    "Ibovespa": calcular_retorno(ibov)
}

# Cria dataframe de retornos e ordena
df_retornos = pd.DataFrame(list(retornos.values()), index=retornos.keys(), columns=["retornos"]).sort_values(by="retornos", ascending=False)

# Plota gráfico de retorno dos bancos
plotar_grafico_retorno(df_retornos, "Retornos dos Bancos")

# Calcula a variação percentual dos lucros
var_lucro_bancos = (lucro_bancos.iloc[-1] / lucro_bancos.iloc[0] - 1).sort_values(ascending=False)

# Plota gráfico da variação dos lucros dos bancos
plotar_grafico_retorno(var_lucro_bancos.to_frame("retornos"), "Lucros dos Bancos")

# Calcula o retorno ano a ano do Itaú e Ibovespa
itau_ano_a_ano = reamostrar_por_periodo(itau, "Y")
ibov_ano_a_ano = reamostrar_por_periodo(ibov, "Y")

# Calcula a diferença de desempenho entre Itaú e Ibovespa
itau_menos_ibov = itau_ano_a_ano - ibov_ano_a_ano
itau_menos_ibov.plot(title="Desempenho Itaú vs Ibovespa")
plt.show()

# Executa análise Long-Short entre Itaú e Banco do Brasil
outperformance = calcular_long_short(itau, banco_brasil, "Y", reamostrar_por_periodo)
plotar_long_short(outperformance, "Long-Short Itaú vs Banco do Brasil")

print("Fim da execução")
