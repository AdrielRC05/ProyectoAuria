from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio
import numpy


# Para que funcione, debes ejecutar en terminales distintas en el siguiente orden:
# ejercicio3.py
# ejercicio2.py
# ejercicio1.py


class NodeState(Struct):
    nombre: str= ""
    x: float= 0.0
    y: float= 0.0

class Trazada(Struct):
    ptoMedioX: float
    ptoMedioY: float

class NodeState2(Struct):
    ptoMedioX: float= 0.0
    ptoMedioY: float= 0.0

# Hago lsa variables globales para que sea más facil trabajar con ellas
global conosAmarillos
conosAmarillos= []
global conosAzules
conosAzules= []
global conosNaranjas
conosNaranjas= []
global conosNaranjasGrandes
conosNaranjasGrandes= []

# Esta función recibe los conos del primer topic y los va almacenando en arrays según su color.
# Una vez los tengo todos, calculo los puntos medios y los guardo en un array, los ordeno 
# utilizando un buvle while y finalmente los mando
@subscribe("datosConos", message_type= NodeState)
async def recibirDatos(msg= NodeState):
    if(msg.nombre!= "FIN"):
        if(msg.nombre=="blue"):
            conosAzules.append([msg.x, msg.y])
        if(msg.nombre=="yellow"):
            conosAmarillos.append([msg.x, msg.y])
        if(msg.nombre=="orange"):
            conosNaranjas.append([msg.x, msg.y])
        if(msg.nombre=="big_orange"):
            conosNaranjasGrandes.append([msg.x, msg.y])
    else:
        # Creo un array numpy de los conoz azules, amarillos y naranjas grandes
        azules = numpy.array(conosAzules)
        amarillos = numpy.array(conosAmarillos)
        naranjasGrandes = numpy.array(conosNaranjasGrandes)
        puntosMedios= []

        # Aquí calculo los puntos medios, aunque aún no están ordenados
        for azul in azules:
            MIN= 9999999.0
            masCercano= None
            for amarillo in amarillos:
                x= amarillo[0]-azul[0]
                y= amarillo[1]-azul[1]
                distancia= (x*x+y*y)**0.5
                if(distancia<MIN):
                    MIN= distancia
                    masCercano= amarillo
            xMedio= (azul[0]+masCercano[0])/2
            yMedio= (azul[1]+masCercano[1])/2
            puntosMedios.append([xMedio,yMedio])
        
        # Calculo el punto medio de los 4 puntos que indican la salida/meta y lo envío
        sumX= 0.0
        sumY= 0.0
        for n in naranjasGrandes:
            sumX= sumX+n[0]
            sumY= sumY+n[1]
        inicioX = sumX/4
        inicioY = sumY/4
        puntoInicio = [inicioX,inicioY]
        await publish("Trazada",NodeState2(float(puntoInicio[0]),float(puntoInicio[1])))

        # La referencia empieza siendo el centro de los naranjas
        referenciaX = inicioX
        referenciaY = inicioY

        # Este bucle lo uso para ordenar los puntos. Busco cuál es el más cercano y así voy ordenando el array
        while len(puntosMedios) > 0:
            distanciaMinima = 9999999.0
            indiceDelMejor = 0
            
            # Elijo cuál es el más cercano
            for i in range(len(puntosMedios)):
                p = puntosMedios[i]
                distX = p[0]-referenciaX
                distY = p[1]-referenciaY
                dist = (distX*distX+distY*distY)**0.5
                
                if dist < distanciaMinima:
                    distanciaMinima = dist
                    indiceDelMejor = i
            
            # Lo borro del array
            puntoElegido = puntosMedios.pop(indiceDelMejor)
            
            # Ponemos ese punto nuevo como la nueva referencia
            referenciaX = puntoElegido[0]
            referenciaY = puntoElegido[1]            
            msg = NodeState2(float(referenciaX), float(referenciaY))
            await publish("Trazada", msg)

        conosAzules.clear()
        conosAmarillos.clear()
        conosNaranjasGrandes.clear()              

# Esto lo pongo también para evitar un posible deadlock
async def iniciar():
    await start()

if __name__ == "__main__":
    asyncio.run(iniciar())

# Para que funcione, debes ejecutar en terminales distintas en el siguiente orden:
# ejercicio3.py
# ejercicio2.py
# ejercicio1.py
