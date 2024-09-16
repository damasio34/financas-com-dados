import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import mplcyberpunk

# Cria um gráfico de barra para exibir retornos com formatação percentual
def plotar_grafico_retorno(df_retornos, titulo):
    plt.style.use("cyberpunk")
    fig, ax = plt.subplots()
    ax.set_title(titulo)
    ax.bar(df_retornos.index, df_retornos["retornos"])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.xticks(fontsize=9)
    plt.show()

# Plota desempenho comparado entre long e short
def plotar_long_short(outperformance, titulo):
    outperformance.plot(title=titulo)
    plt.show()
