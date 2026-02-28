from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio
import numpy

class NodeState(Struct):
    nombre: str= ""
    x: float= 0.0
    y: float= 0.0

class Trazada(Struct):
    nombre: str
    listaPuntos: list[list[float]]

arrayPuntos= []

@subscribe("datosCono", message_type= NodeState)
async def recibirDatos(msg= NodeState):
    if(msg.nombre!= "FIN"):
        arrayPuntos.append([msg.x, msg.y])
    else:
        listCoordX= numpy.unique(arrayPuntos[:,0])
                    
                
        trazada= numpy.array(arrayPuntos)
        trazada= trazada.tolist()


