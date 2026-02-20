# Programa para Dimensionamento Elétrico Residencial conforme NBR 5410
# Focado em Iluminação, Tomadas de Uso Geral (TUG) e Tomadas de Uso Específico (TUE)
# Versão atualizada: usuário informa comprimento e largura (calcula área e perímetro)
# Autor: Moises (baseado em NBR 5410 - regras extraídas de fontes confiáveis)

import math

def calcular_iluminacao(area):
    """Calcula potência mínima de iluminação em VA conforme NBR 5410."""
    if area <= 6:
        return 100
    else:
        adicional = math.floor((area - 6) / 4)
        return 100 + 60 * adicional

def calcular_tug_min(perimetro, eh_umido):
    """Calcula quantidade mínima de TUG (tomadas de uso geral)."""
    if eh_umido:
        divisor = 3.5
    else:
        divisor = 5.0
    return math.ceil(perimetro / divisor)

def calcular_potencia_tug(qtd_tug, eh_umido):
    """Calcula potência total para TUG em VA."""
    if eh_umido:
        # 600 VA para as primeiras 3, 100 VA para excedentes
        return min(qtd_tug, 3) * 600 + max(0, qtd_tug - 3) * 100
    else:
        return qtd_tug * 100

def main():
    print("Dimensionador Elétrico Residencial (NBR 5410)")
    print("Use ponto para decimais (ex: 4.2).")
    print("Cômodos úmidos típicos: cozinha, área de serviço, lavanderia, banheiro, copa.\n")

    try:
        num_comodos = int(input("Quantos cômodos deseja dimensionar? "))
    except ValueError:
        print("Número inválido. Encerrando.")
        return

    total_ilum_va = 0
    total_tug_va = 0
    total_tue_va = 0
    detalhes = []

    for i in range(num_comodos):
        print(f"\n--- Cômodo {i+1} ---")
        nome = input("Nome do cômodo (ex: Quarto, Cozinha): ").strip()

        while True:
            try:
                comprimento = float(input("Comprimento (m): "))
                if comprimento <= 0:
                    print("Comprimento deve ser maior que zero.")
                    continue
                largura = float(input("Largura (m): "))
                if largura <= 0:
                    print("Largura deve ser maior que zero.")
                    continue
                break
            except ValueError:
                print("Digite um número válido (ex: 5.0 ou 4.2).")

        area = comprimento * largura
        perimetro = 2 * (comprimento + largura)

        eh_umido_str = input("É cômodo úmido? (s/n): ").strip().lower()
        eh_umido = eh_umido_str in ['s', 'sim', 'y', 'yes']

        # Iluminação
        ilum_va = calcular_iluminacao(area)
        total_ilum_va += ilum_va

        # TUG
        tug_min = calcular_tug_min(perimetro, eh_umido)
        # Regra extra: áreas ≤ 6 m² não úmidas → mínimo 1 tomada
        if area <= 6 and not eh_umido:
            tug_min = max(1, tug_min)

        print(f"→ Área calculada: {area:.2f} m²")
        print(f"→ Perímetro calculado: {perimetro:.2f} m")
        print(f"→ Quantidade mínima de TUG recomendada: {tug_min}")

        while True:
            try:
                qtd_tug = int(input(f"Quantidade de TUG a instalar (mínimo {tug_min}): "))
                if qtd_tug < tug_min:
                    print(f"Usando o mínimo recomendado ({tug_min}).")
                    qtd_tug = tug_min
                break
            except ValueError:
                print("Digite um número inteiro.")

        tug_va = calcular_potencia_tug(qtd_tug, eh_umido)
        total_tug_va += tug_va

        # TUE (Tomadas de Uso Específico)
        tue_va_comodo = 0
        tue_detalhes = []
        try:
            num_tue = int(input("Quantas TUE neste cômodo? (0 se nenhuma): "))
        except ValueError:
            num_tue = 0

        for j in range(num_tue):
            tue_nome = input(f"   Nome da TUE {j+1} (ex: Chuveiro, Ar-condicionado): ").strip()
            while True:
                try:
                    tue_pot = float(input(f"   Potência da {tue_nome} (VA ou W): "))
                    if tue_pot <= 0:
                        print("Potência deve ser maior que zero.")
                        continue
                    break
                except ValueError:
                    print("Digite um número válido.")
            tue_va_comodo += tue_pot
            tue_detalhes.append(f"{tue_nome}: {tue_pot:.0f} VA")

        total_tue_va += tue_va_comodo

        # Armazena para relatório
        detalhes.append({
            "Nome": nome,
            "Comprimento": comprimento,
            "Largura": largura,
            "Área": area,
            "Perímetro": perimetro,
            "Ilum VA": ilum_va,
            "TUG Qtd": qtd_tug,
            "TUG VA": tug_va,
            "TUE VA": tue_va_comodo,
            "TUE Detalhes": ", ".join(tue_detalhes) if tue_detalhes else "-"
        })

    # Cálculo de potência ativa (estimativa simples de fator de potência)
    total_ilum_w = total_ilum_va * 1.0
    total_tug_w  = total_tug_va  * 0.8   # típico para tomadas gerais
    total_tue_w  = total_tue_va  * 1.0   # eletrodomésticos geralmente FP ≈ 1
    total_w = total_ilum_w + total_tug_w + total_tue_w

    # Relatório final
    print("\n" + "="*70)
    print("RESUMO DO DIMENSIONAMENTO ELÉTRICO")
    print("="*70)
    print(f"{'Cômodo':<18} {'Compr. × Larg.':<12} {'Área':<8} {'Perim.':<8} {'Ilum VA':<9} {'TUG Qtd':<8} {'TUG VA':<9} {'TUE VA':<9} {'TUE'}")
    print("-"*100)
    for d in detalhes:
        print(f"{d['Nome']:<18} {d['Comprimento']:.1f} × {d['Largura']:<8.1f} {d['Área']:<8.2f} {d['Perímetro']:<8.2f} {d['Ilum VA']:<9} {d['TUG Qtd']:<8} {d['TUG VA']:<9} {d['TUE VA']:<9} {d['TUE Detalhes']}")

    print("\nTOTAlS GERAIS:")
    print(f"• Iluminação ................: {total_ilum_va:>6.0f} VA  ({total_ilum_w:>6.0f} W)")
    print(f"• Tomadas de Uso Geral (TUG).: {total_tug_va:>6.0f} VA  ({total_tug_w:>6.0f} W)")
    print(f"• Tomadas de Uso Específico.: {total_tue_va:>6.0f} VA  ({total_tue_w:>6.0f} W)")
    print(f"Potência total estimada .....: {total_w:>6.0f} W")
    print("\nLembrete: Este é um cálculo preliminar. Consulte um engenheiro eletricista para o projeto completo, incluindo circuitos, seção de condutores, proteção e aterramento.")

if __name__ == "__main__":
    main()