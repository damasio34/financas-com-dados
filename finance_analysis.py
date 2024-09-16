# Calcula o retorno percentual de uma lista de cotações
def calcular_retorno(cotacoes):
    return round((cotacoes[-1] / cotacoes[0] - 1) * 100, 2)

# Calcula a diferença entre o desempenho de dois ativos (long-short)
def calcular_long_short(long, short, periodo, reamostrar_por_periodo):
    var_long = reamostrar_por_periodo(long, periodo)
    var_short = reamostrar_por_periodo(short, periodo)
    return var_long - var_short
