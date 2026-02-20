
# Online Python - IDE, Editor, Compiler, Interpreter


a = float(input('valor inicial: '))
b = float(input('taxa de juros anual: '))
c = float(input('período, em anos: '))
d = (a*(1+(b/100))**c)

if c > 1:
    texto = "anos"
else:
    texto = "ano"

print(f'Um valor de R$ {a:.2f} investido por um período de {c:.1f} {texto} \na uma taxa de juros de {b:.2f}% a.a, será de R$ {d:.2f}')
print("")
print(f'Total de juros: R$ {(d - a):.2f}')