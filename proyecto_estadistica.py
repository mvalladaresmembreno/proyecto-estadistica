# Con paciencia y saliba el elefante se la metio a la hormiga -- Margarita

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg 
from statistics import mode
import math
import typing

#Iniciar la aplicación
app = QtWidgets.QApplication([])

#Icono del proyecto
app.setWindowIcon(QIcon("Logo_UNI.png"))

#Cargar archivos .ui
pres = uic.loadUi("presentacion.ui")
add = uic.loadUi("insercionDatos.ui")
prin = uic.loadUi("proyectoEstadistica.ui")
graf = uic.loadUi("graficas.ui")
calc = uic.loadUi("cuartiles.ui")
perc = uic.loadUi("percentil.ui")
deci = uic.loadUi("deciles.ui")

#Variables globales
listDatos = []
listFi = []
listAux = []

#Al presionar el boton continuar va a ocultar la pantalla de de presentacion
#Para dar paso al siguiente
def gui_insercion():
    pres.hide()
    add.show()

def gui_graficas():
    graf.show()


#Cuando presione el boton agregar el valor escrito será guardado en una lista
#Y el editText será borrado para insertar otro dato
def addValor():
    valorString = add.etDatos.text()
    valor = int(valorString)
    if(len(listDatos) == 19):
        listDatos.append(valor)
        add.etDatos.setText("")
        add.hide()
        prin.show()
    else:
        listDatos.append(valor)
        add.etDatos.setText("")

# Calculamos Frecuencia Absoluta
def obtenerFrec(data: list[float]) -> typing.Dict[float, int]:
    frec = {}.fromkeys(data, 0)
    for value in data:
        frec[value] += 1
    return frec

# Calculamos Frecuencia Acumulada
def frecAcumulado(datos, freq):
    frecAcumulada = {}.fromkeys(datos, 0)
    frecAcumulada[datos[0]] = freq[datos[0]]
    keys = list(freq.keys())
    for i in range(1, len(keys)):
        frecAcumulada[keys[i]] = frecAcumulada[keys[i - 1]] + freq[keys[i]]
    return frecAcumulada

# Calculamos la Varianza ---Felix
def variancita(datos: list[float]) -> list[float]:
    datosLenght = len(datos)
    suma = 0
    for n in range(len(listDatos)):
        suma += listDatos[n]
    media = suma/datosLenght
    return sum([(k - media)**2 for k in datos]) / (datosLenght)

def gui_cuartil():
    calc.show()
    calc.btnCalcular.clicked.connect(cuartilResultado)

def gui_percentil():
    perc.show()
    perc.btnCalcular.clicked.connect(percentilResultado)

def gui_decil():
    deci.show()
    deci.btnCalcular.clicked.connect(decilResultado)

# Calculamos los Percentiles -- Jeison
def percentilResultado():
    cant = perc.etDato.text()
    cantidad = int(cant)
    if(cantidad <= 100 and cantidad >= 1):
        percen = cantidad*(len(listDatos))/100
        if (percen % 1 == 0):
            parce = int(percen)
            prin.tvPercentil.setText("pos: "+str(percen)+" valor: "+str(listDatos[parce-1]))
        else:
            parce= math.floor(percen)
            sumita = (listDatos[parce]+listDatos[parce-1])/2
            prin.tvPercentil.setText("pos: "+str(parce)+" valor: "+str(sumita))
    else:
        prin.tvVal.setText("Ingrese del 1 al 100")
    perc.hide()

# Calculamos los Deciles
def decilResultado():
    cant = deci.etDato.text()
    cantidad = int(cant)
    if(cantidad <= 10 and cantidad >= 1):
        deciles = cantidad*(len(listDatos))/10
        if (deciles % 1 == 0):
            print(deciles)
            diles = int(deciles)
            prin.tvDecil.setText("pos: "+str(deciles)+" valor: "+str(listDatos[diles-1]))
        else:
            diles= math.floor(deciles)
            sumita = (listDatos[diles]+listDatos[diles-1])/2
            prin.tvDecil.setText("pos: "+str(diles)+" valor: "+str(sumita))
    else:
        prin.tvVal.setText("Ingrese del 1 al 10")
    deci.hide()

# Calculamos los Cuartiles
def cuartilResultado():
    cant = calc.etDato.text()
    cantidad = int(cant)
    if(cantidad <= 4 and cantidad >= 1):
        cuarto = cantidad*(len(listDatos))/4
        if (cuarto % 1 == 0):
            print(cuarto)
            cua = int(cuarto)
            prin.tvCuartil.setText("pos: "+str(cuarto)+" valor: "+str(listDatos[cua-1]))
        else:
            cua= math.floor(cuarto)
            sumita = (listDatos[cua]+listDatos[cua-1])/2
            prin.tvCuartil.setText("pos: "+str(cua)+" valor: "+str(sumita))
    else:
        prin.tvVal.setText("Ingrese del 1 al 4")
    calc.hide()

#Se calcula, la media, la mediana, la moda y la varianza --- Harvin
def medidasAgrupadas():
    suma = 0
    for n in range(len(listDatos)):
        suma += listDatos[n]
    media = suma/20
    mediana = ((20/2)+(20/2)+1)/2
    moda = mode(listDatos)
    varianza = variancita(listDatos)
    desviacionEstandar = varianza**(1/2)
    prin.tvVarianza.setText(str(round(varianza,2)))
    prin.tvDesviacionEstandar.setText(str(round(desviacionEstandar,2)))
    prin.tvModa.setText(str(moda))
    prin.tvMedia.setText(str(media))
    prin.tvMediana.setText(str(mediana))

def datosTabla():
    #Aqui se llenan los datos de la tabla
    prin.tablitaFrecuencias.setRowCount(len(listDatos)+1)
    prin.tablitaFrecuencias.setColumnCount(7)
    prin.tablitaFrecuencias.setHorizontalHeaderLabels(('Datos','fi','Fi','fr','Fr','%','porcentaje acum'))
    prin.tablitaFrecuencias.setEditTriggers(QAbstractItemView.NoEditTriggers)

    listDatos.sort()
    frecuencia = obtenerFrec(listDatos)
    frecuencia_acum = frecAcumulado(listDatos, frecuencia)#--- Felix
    filas = 0
    sumafi = 0
    sumafr = 0
    sumapor = 0
    for i in list(frecuencia.keys()):
        prin.tablitaFrecuencias.setItem(filas,0,QTableWidgetItem(str(i)))
        prin.tablitaFrecuencias.setItem(filas,1,QTableWidgetItem(str(frecuencia[i])))
        prin.tablitaFrecuencias.setItem(filas,2,QTableWidgetItem(str(frecuencia_acum[i])))
        filas += 1
        sumafi += frecuencia[i]
    filas=0
    for i in list(frecuencia.keys()):
        frecuenciaRelativa = frecuencia[i]/sumafi
        frecuenciaPorcentual = frecuenciaRelativa*100
        prin.tablitaFrecuencias.setItem(filas,3,QTableWidgetItem(str(round(frecuenciaRelativa,2))))
        prin.tablitaFrecuencias.setItem(filas,5,QTableWidgetItem(str(round(frecuenciaPorcentual,2))))
        sumafr += frecuenciaRelativa
        sumapor += frecuenciaPorcentual
        prin.tablitaFrecuencias.setItem(filas,4,QTableWidgetItem(str(round(sumafr,2))))
        prin.tablitaFrecuencias.setItem(filas,6,QTableWidgetItem(str(round(sumapor,2))))
        filas += 1

    prin.tablitaFrecuencias.setItem(filas,1,QTableWidgetItem(str(sumafi)))
    prin.tablitaFrecuencias.setItem(filas,3,QTableWidgetItem(str(round(sumafr,2))))
    prin.tablitaFrecuencias.setItem(filas,5,QTableWidgetItem(str(round(sumapor,2))))

#---- JoJo    

def grafica():

    pl = pg.plot()

    frecuencia = obtenerFrec(listDatos)

    for i in list(frecuencia.keys()):
        listFi.append(frecuencia[i])
    for i in listDatos:
        if (i in listAux):
            print("Nada")
        else:
            listAux.append(i)
    
    bargraph = pg.BarGraphItem(x = listAux, height = listFi, width = 0.6, brush = 'g')
    pl.addItem(bargraph)

    graf.graficaUno.addWidget(pl)

#Botones
pres.btnContinuar.clicked.connect(gui_insercion)
add.btnInsertar.clicked.connect(addValor)
prin.btnCalcular.clicked.connect(medidasAgrupadas)
prin.btnTabla.clicked.connect(datosTabla)
prin.btnGuiGraficas.clicked.connect(gui_graficas)
prin.btnCalcularCuar.clicked.connect(gui_cuartil)
prin.btnCalcularPerce.clicked.connect(gui_percentil)
prin.btnCalcularDecil.clicked.connect(gui_decil)
graf.btnGrafica.clicked.connect(grafica)

pres.show()
app.exec()
