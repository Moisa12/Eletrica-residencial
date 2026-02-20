
# Online Python - IDE, Editor, Compiler, Interpreter


a = float(input('valor inicial: '))
b = float(input('taxa de juros anual: '))
c = float(input('período, em anos: '))
d = (a*(1+(b/100)*c))


print(f'Valor investido R$ {a:.2f}')
print(f'Valor final R$ {d:.2f}')
print(f'Total de juros: R$ {(d - a):.2f}')