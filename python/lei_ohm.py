import math

print("------------------------------------------")
print("   CALCULADORA DA LEI DE OHM (V, I, R, P) ")
print("------------------------------------------")
print("Instruções: Digite o valor conhecido ou '?' para o que deseja descobrir.")

def calcular():
    try:
        v = input("Tensão (V): ")
        i = input("Corrente (A): ")
        r = input("Resistência (Ω): ")

        # Cálculo da Resistência
        if r == "?":
            v, i = float(v), float(i)
            res = v / i
            print(f"\n> Resultado: Resistência = {res:.2f} Ω")
            print(f"> Potência Dissipada = {v * i:.2f} W")
        
        # Cálculo da Tensão
        elif v == "?":
            r, i = float(r), float(i)
            res = r * i
            print(f"\n> Resultado: Tensão = {res:.2f} V")
            print(f"> Potência Dissipada = {res * i:.2f} W")
            
        # Cálculo da Corrente
        elif i == "?":
            v, r = float(v), float(r)
            res = v / r
            print(f"\n> Resultado: Corrente = {res:.2f} A")
            print(f"> Potência Dissipada = {v * res:.2f} W")

    except ValueError:
        print("\nErro: Por favor, use números e coloque '?' apenas em um dos campos.")
    except ZeroDivisionError:
        print("\nErro: Resistência ou Corrente não podem ser zero.")

calcular()
input("\nPressione Enter para fechar...")