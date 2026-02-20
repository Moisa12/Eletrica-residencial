import math

def obter_secao_minima(tipo_circuito):
    """Tabela 47 NBR 5410 - seção mínima para condutores de cobre"""
    tipo = tipo_circuito.lower()
    if tipo in ["iluminação", "lâmpadas", "luz"]:
        return 1.5
    elif tipo in ["tomada", "força", "tug", "equipamento", "chuveiro"]:
        return 2.5
    else:
        return 1.5  # padrão conservador


def obter_capacidade_corrente(secao):
    """Tabela 36 NBR 5410 – método B1, 2 condutores carregados, cobre PVC 70°C, 30°C ambiente"""
    tabela = {
        1.5: 17.5,
        2.5: 24.0,
        4.0: 32.0,
        6.0: 41.0,
        10.0: 57.0,
        16.0: 76.0,
        25.0: 101.0,
        35.0: 125.0,
        50.0: 151.0,
        70.0: 192.0,
    }
    secoes = sorted(tabela.keys())
    for s in secoes:
        if secao <= s:
            return tabela[s]
    return tabela[secoes[-1]]


def fator_correcao_temperatura(temp_ambiente):
    """Tabela 40 NBR 5410 – isolação PVC, linhas não subterrâneas (ambiente ar)"""
    tabela_fct = {
        10: 1.22,
        15: 1.17,
        20: 1.12,
        25: 1.06,
        30: 1.00,
        35: 0.94,
        40: 0.87,
        45: 0.79,
        50: 0.71,
        55: 0.61,
        60: 0.50,
    }
    if temp_ambiente <= 10:
        return 1.22
    if temp_ambiente >= 60:
        return 0.50
    # Interpolação simples entre pontos mais próximos
    temps = sorted(tabela_fct.keys())
    for i in range(len(temps)-1):
        if temps[i] <= temp_ambiente <= temps[i+1]:
            t1, t2 = temps[i], temps[i+1]
            f1, f2 = tabela_fct[t1], tabela_fct[t2]
            return f1 + (f2 - f1) * (temp_ambiente - t1) / (t2 - t1)
    return 1.00  # default se fora da faixa


def fator_correcao_agrupamento(num_circuitos):
    """Tabela 42 NBR 5410 – linha 1 (feixe em conduto fechado ou ao ar livre)"""
    tabela_fca = {
        1: 1.00,
        2: 0.80,
        3: 0.70,
        4: 0.65,
        5: 0.60,
        6: 0.57,
        7: 0.54,
        8: 0.52,
        9: 0.50,
        12: 0.45,
        16: 0.41,
        20: 0.38,
    }
    if num_circuitos <= 1:
        return 1.00
    if num_circuitos >= 20:
        return 0.38
    # Pega o valor mais próximo (conservador: arredonda para cima no número)
    for n in sorted(tabela_fca.keys(), reverse=True):
        if num_circuitos >= n:
            return tabela_fca[n]
    return 1.00


def calcular_queda_tensao(U_nominal, comprimento, corrente, secao):
    """ΔU(%) ≈ (2 × ρ × L × I) / (S × U) × 100    ρ ≈ 0,017 para cobre ~70°C"""
    rho = 0.017
    delta_u = (2 * rho * comprimento * corrente) / (secao * U_nominal) * 100
    return delta_u


def sugerir_disjuntor(corrente_projeto):
    disjuntores = [10, 16, 20, 25, 32, 40, 50, 63, 80, 100]
    for d in disjuntores:
        if d >= corrente_projeto * 1.25:
            return d
    return 100


def main():
    print("=== Calculadora NBR 5410 - Seção + Disjuntor (com FCT e FCA) ===\n")
    
    tipo = input("Tipo de circuito (iluminação / tomada / força): ").strip()
    tensao = float(input("Tensão nominal (127 ou 220 V): "))
    potencia = float(input("Potência total da carga (W): "))
    comprimento = float(input("Comprimento do circuito (ida) em metros: "))
    temp_ambiente = float(input("Temperatura ambiente (°C) [normal: 30]: ") or 30)
    num_circuitos_agrupados = int(input("Quantos circuitos/cabos agrupados no mesmo eletroduto/canaleta? [1 se único]: ") or 1)
    
    corrente = potencia / tensao
    secao_min_norma = obter_secao_minima(tipo)
    
    fct = fator_correcao_temperatura(temp_ambiente)
    fca = fator_correcao_agrupamento(num_circuitos_agrupados)
    fator_total = fct * fca
    
    corrente_corrigida = corrente / fator_total if fator_total > 0 else corrente
    
    print(f"\nResultados iniciais:")
    print(f"• Corrente de projeto ........: {corrente:.2f} A")
    print(f"• Fator temperatura (FCT) ....: {fct:.2f} (para {temp_ambiente}°C)")
    print(f"• Fator agrupamento (FCA) ....: {fca:.2f} (para {num_circuitos_agrupados} circuitos)")
    print(f"• Fator total (FCT × FCA) ....: {fator_total:.2f}")
    print(f"• Corrente corrigida necessária: {corrente_corrigida:.2f} A")
    print(f"• Seção mínima norma (T47) ...: {secao_min_norma} mm²\n")
    
    secoes_comerciais = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50]
    
    print("Análise das seções comerciais (método B1):")
    print("Seção (mm²) | Iz base (A) | Iz corrigido (A) | Queda % | Status")
    print("-" * 65)
    
    secao_escolhida = None
    queda_final = None
    
    for secao in secoes_comerciais:
        if secao < secao_min_norma:
            status = f"Rejeitado (< {secao_min_norma} mm² norma)"
        else:
            iz_base = obter_capacidade_corrente(secao)
            iz_corrigido = iz_base * fator_total   # capacidade real do condutor no local
            if corrente > iz_corrigido:
                status = f"Rejeitado (I > {iz_corrigido:.1f} A corrigido)"
            else:
                queda = calcular_queda_tensao(tensao, comprimento, corrente, secao)
                if queda > 4.0:
                    status = f"Rejeitado (queda {queda:.2f}% > 4%)"
                else:
                    status = f"OK (queda {queda:.2f}%)"
                    if secao_escolhida is None:
                        secao_escolhida = secao
                        queda_final = queda
        
        iz_base = obter_capacidade_corrente(secao)
        iz_corrigido = iz_base * fator_total
        print(f"{secao:11.1f} | {iz_base:11.1f} | {iz_corrigido:16.1f} | {calcular_queda_tensao(tensao, comprimento, corrente, secao):7.2f}% | {status}")
    
    if secao_escolhida:
        disjuntor = sugerir_disjuntor(corrente)
        print(f"\n*** Recomendação final (menor seção que atende todos critérios) ***")
        print(f"• Seção recomendada ............: {secao_escolhida} mm²")
        print(f"• Disjuntor sugerido ...........: {disjuntor} A (curva C)")
        print(f"• Queda de tensão ..............: {queda_final:.2f}%")
        print(f"• Capacidade corrigida do cabo .: {obter_capacidade_corrente(secao_escolhida) * fator_total:.1f} A")
    else:
        print("\nNenhuma seção da lista atende. Considere: menor temperatura ambiente, menos agrupamento, ou seção maior.")

if __name__ == "__main__":
    main()