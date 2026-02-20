import math

def calcular_transformador():
    print("--- SIMULADOR DE TRANSFORMADOR TRIFÁSICO ---")
    
    # 1. Entrada de Dados
    kva = float(input("Potência do transformador (kVA): "))
    v_primario_linha = float(input("Tensão de linha no Primário (V): "))
    v_secundario_linha = float(input("Tensão de linha no Secundário (V): "))
    
    print("\nTipos de Ligação:")
    print("1 - Estrela-Estrela (Y-Y)")
    print("2 - Estrela-Triângulo (Y-Δ)")
    print("3 - Triângulo-Triângulo (Δ-Δ)")
    print("4 - Triângulo-Estrela (Δ-Y)")
    opcao = input("Escolha a ligação (1-4): ")

    raiz3 = math.sqrt(3)
    s_total = kva * 1000  # Converte kVA para VA

    # 2. Lógica de Tensões de Fase (Baseado na ligação)
    # Primário
    if opcao in ['1', '2']: # Estrela no primário
        v_primario_fase = v_primario_linha / raiz3
    else: # Triângulo no primário
        v_primario_fase = v_primario_linha

    # Secundário
    if opcao in ['1', '4']: # Estrela no secundário
        v_secundario_fase = v_secundario_linha / raiz3
    else: # Triângulo no secundário
        v_secundario_fase = v_secundario_linha

    # 3. Cálculo de Correntes de Linha (Independe da ligação, depende da potência total)
    # I_linha = S / (V_linha * raiz3)
    i_primario_linha = s_total / (v_primario_linha * raiz3)
    i_secundario_linha = s_total / (v_secundario_linha * raiz3)

    # 4. Cálculo de Correntes de Fase (Depende da ligação)
    # No primário
    if opcao in ['1', '2']: # Estrela: I_fase = I_linha
        i_primario_fase = i_primario_linha
    else: # Triângulo: I_fase = I_linha / raiz3
        i_primario_fase = i_primario_linha / raiz3

    # No secundário
    if opcao in ['1', '4']: # Estrela: I_fase = I_linha
        i_secundario_fase = i_secundario_linha
    else: # Triângulo: I_fase = I_linha / raiz3
        i_secundario_fase = i_secundario_linha / raiz3

    # 5. Exibição dos Resultados
    print("\n" + "="*30)
    print(f"RESULTADOS PARA {kva} kVA")
    print("="*30)
    print(f"--- PRIMÁRIO ---")
    print(f"Tensão de Linha:   {v_primario_linha:>8.2f} V")
    print(f"Tensão de Fase:    {v_primario_fase:>8.2f} V")
    print(f"Corrente de Linha: {i_primario_linha:>8.2f} A")
    print(f"Corrente de Fase:  {i_primario_fase:>8.2f} A")
    print(f"\n--- SECUNDÁRIO ---")
    print(f"Tensão de Linha:   {v_secundario_linha:>8.2f} V")
    print(f"Tensão de Fase:    {v_secundario_fase:>8.2f} V")
    print(f"Corrente de Linha: {i_secundario_linha:>8.2f} A")
    print(f"Corrente de Fase:  {i_secundario_fase:>8.2f} A")
    print("="*30)

# Executa o programa
if __name__ == "__main__":
    calcular_transformador()