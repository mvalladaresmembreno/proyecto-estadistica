
datos = []
suma = 0
for i in range(5):
    datito = int(input("Ingrese el valor "+str(i)+": "))
    datos.append(datito)
    suma += datito
media = suma/5
print(media)
suma=0
for i in datos:
    suma += (i - media)**2
varianza = suma/5
print(varianza)
