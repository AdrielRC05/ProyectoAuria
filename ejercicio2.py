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
    x: float
    ptoMedioY: float

class NodeState2(Struct):
    x: float= 0.0
    ptoMedioY: float= 0.0

# Hago global la variable para que sea más facil trabajar con ella
global arrayPuntos
arrayPuntos= []

# Esta función recibe los conos del primer topic y los va almacenando en la variable global hasta que llega al final.
# Una vez deja de recibir conos, convierte la lista a una lista de numpy para trabajar con ellos, y hace lo siguiente:
# - Escoge todos los valores de x
# - Para cada valor de x, busca los dos valores de y asociados, los suma y divide por 2
# - Publica en un nuevo topic cada valor de x con el punto medio calculado en el paso anterior
@subscribe("datosConos", message_type= NodeState)
async def recibirDatos(msg= NodeState):
    if(msg.nombre!= "FIN"):
        arrayPuntos.append([msg.x, msg.y])
    else:
        arrayFinal= numpy.array(arrayPuntos)
        listCoordX= numpy.unique(arrayFinal[:,0])
        for x in listCoordX:
            ptoMedio= 0
            for cono in arrayPuntos:
                if(cono[0]== x):
                    ptoMedio= ptoMedio+cono[1]
            # Divido entre 2 porque en el csv hay 2 valores exactos de y por cada valor de x
            ptoMedio= ptoMedio/2
            conoAEnviar= NodeState2(float(x), float(ptoMedio))
            await publish("Trazada",conoAEnviar)
        arrayPuntos.clear()

# Esto lo pongo también para evitar un posible deadlock
async def iniciar():
    await start()

if __name__ == "__main__":
    asyncio.run(iniciar())

# Para que funcione, debes ejecutar en terminales distintas en el siguiente orden:
# ejercicio3.py
# ejercicio2.py
# ejercicio1.py
