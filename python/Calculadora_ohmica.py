#!/usr/bin/python
# -*- coding: latin-1 -*-

print("Calculadora Ohmica")
print("")
print("Digite: \n1 - para calcular resistência elétrica")
print("2 - para calcular tensão elétrica ou ")
escolha = int(input("3 - para calcular corrente elétrica e em seguida tecle ENTER: "))
print("")
if(escolha == 1):
	V = float(input("Digite o valor da tensão elétrica (em Volts): "))
	I = float(input("Digite o valor da corrente elétrica (em Amperes): "))
	print "O valor da resistência elétrica é: ", V/I, "o"
elif(escolha == 2):
	R = float(input("Digite o valor da resistência elétrica (em Ohms): "))
	I = float(input("Digite o valor da corrente elétrica (em Amperes): "))
	print "O valor da tensão elétrica é: ", R*I, "V"
else:
	V = float(input("Digite o valor da tensão elétrica (em Volts): "))
	R = float(input("Digite o valor da resistência elétrica (em Ohms): "))
	print "O valor da corrente elétrica é: ", V/R, "A"
