import os

def limpar_tela():
    # Comando para limpar a tela (funciona em Windows e Linux/Mac)
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_tabela(movimentacoes):
    limpar_tela()
    print("-" * 70)
    print(f"{'DATA':<12} | {'DESCRIÇÃO':<30} | {'TIPO':<10} | {'VALOR (R$)':>10}")
    print("-" * 70)

    saldo = 0.0

    for mov in movimentacoes:
        data = mov['data']
        desc = mov['descricao']
        tipo = mov['tipo']
        valor = mov['valor']

        # Atualiza o saldo
        if tipo == 'Entrada':
            saldo += valor
            cor_tipo = "Entrada" # Apenas texto normal
        else:
            saldo -= valor
            cor_tipo = "Saída"

        # Formatação da linha
        print(f"{data:<12} | {desc:<30} | {cor_tipo:<10} | {valor:>10.2f}")

    print("-" * 70)
    print(f"{'SALDO FINAL:':<56} | {saldo:>10.2f}")
    print("-" * 70)
    input("\nPressione Enter para voltar ao menu...")

def main():
    fluxo_caixa = []

    while True:
        limpar_tela()
        print("=== SISTEMA DE FLUXO DE CAIXA ===")
        print("1. Adicionar Movimentação")
        print("2. Ver Relatório (Tabela)")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- Nova Movimentação ---")
            data = input("Data (ex: 25/10): ")
            descricao = input("Descrição (ex: Venda de Bolo): ")
            
            # Tratamento de erro para garantir que o valor seja número
            while True:
                try:
                    valor_input = input("Valor (R$): ").replace(',', '.') # Aceita vírgula ou ponto
                    valor = float(valor_input)
                    break
                except ValueError:
                    print("Erro: Digite um número válido.")

            tipo_input = input("É Entrada (E) ou Saída (S)? ").upper()
            tipo = 'Entrada' if tipo_input == 'E' else 'Saída'

            # Salva num dicionário e adiciona à lista
            movimentacao = {
                "data": data,
                "descricao": descricao,
                "valor": valor,
                "tipo": tipo
            }
            fluxo_caixa.append(movimentacao)
            print("Movimentação registrada com sucesso!")
            input("Pressione Enter...")

        elif opcao == '2':
            if not fluxo_caixa:
                print("\nNenhuma movimentação registrada ainda.")
                input("Pressione Enter...")
            else:
                exibir_tabela(fluxo_caixa)

        elif opcao == '3':
            print("Saindo do sistema. Até mais!")
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
