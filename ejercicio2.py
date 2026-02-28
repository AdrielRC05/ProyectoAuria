from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio
import numpy

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

global arrayPuntos

@subscribe("datosCono", message_type= NodeState)
async def recibirDatos(msg= NodeState):
    if(msg.nombre!= "FIN"):
        arrayPuntos.append([msg.x, msg.y])
    else:
        arrayPuntos= numpy.array(arrayPuntos)
        listCoordX= numpy.unique(arrayPuntos[:,0])
        for x in listCoordX:
            ptoMedio= 0
            for cono in arrayPuntos:
                if(cono[0]== x):
                    ptoMedio= ptoMedio+cono[1]
            # Divido entre 2 porque en el csv hay 2 valores exactos de y por cada valor de x
            ptoMedio= ptoMedio/2
            conoAEnviar= NodeState2(x, ptoMedio)
            await publish("Trazada",conoAEnviar)
            print("Enviando x2...")

async def iniciar():
    await start()

if __name__ == "__main__":
    asyncio.run(iniciar())
