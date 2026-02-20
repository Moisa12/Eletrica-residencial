import math

def dimensionar_cabo():
    print("--- DIMENSIONADOR DE CONDUTORES (NBR 5410 SIMPLIFICADO) ---")
    
    # 1. ENTRADA DE DADOS
    distancia = float(input("Distância do circuito (metros): "))
    tensao = float(input("Tensão do circuito (V): "))
    corrente = float(input("Corrente da carga (A): "))
    queda_max_percentual = float(input("Queda de tensão máxima permitida (%): "))
    
    # Tabela simplificada: Seção (mm²) vs Capacidade de Corrente (A) 
    # (Ref: NBR 5410, Cobre, PVC, 2 cond. carregados em eletroduto)
    tabela_ampacidade = [
        (1.5, 17.5), (2.5, 24), (4, 32), (6, 41), (10, 57), 
        (16, 76), (25, 101), (35, 125), (50, 151), (70, 192)
    ]
    
    # --- CRITÉRIO 1: CAPACIDADE DE CONDUÇÃO ---
    secao_corrente = 1.5
    for secao, amp in tabela_ampacidade:
        if amp >= corrente:
            secao_corrente = secao
            break
    else:
        print("Erro: Corrente acima da capacidade da tabela (máx 192A).")
        return

    # --- CRITÉRIO 2: QUEDA DE TENSÃO ---
    # Fórmula simplificada: S = (2 * L * I * rho) / delta_V
    # Onde rho (cobre) é aprox. 1/56 (0.0178)
    rho = 0.0178
    queda_v_max = (queda_max_percentual / 100) * tensao
    
    # Cálculo da seção teórica para atender a queda de tensão
    secao_queda = (2 * distancia * corrente * rho) / queda_v_max
    
    # Encontrar no catálogo a seção comercial imediatamente superior à teórica
    secao_queda_comercial = 1.5
    for secao, amp in tabela_ampacidade:
        if secao >= secao_queda:
            secao_queda_comercial = secao
            break

    # --- RESULTADO FINAL ---
    # O cabo escolhido deve ser o MAIOR entre os dois critérios
    secao_final = max(secao_corrente, secao_queda_comercial)

    print("\n" + "="*40)
    print(f"ANÁLISE PARA {corrente}A EM {distancia}m")
    print("="*40)
    print(f"Pelo critério de Corrente:  {secao_corrente} mm²")
    print(f"Pelo critério de Queda:     {secao_queda_comercial} mm² (Teórico: {secao_queda:.2f}mm²)")
    print("-" * 40)
    print(f"SEÇÃO RECOMENDADA: {secao_final} mm²")
    
    # Cálculo da queda real com o cabo escolhido
    queda_real = (2 * distancia * corrente * rho) / secao_final
    perc_real = (queda_real / tensao) * 100
    print(f"Queda de Tensão Final: {queda_real:.2f}V ({perc_real:.2f}%)")
    print("="*40)

if __name__ == "__main__":
    dimensionar_cabo()