from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio
import numpy

class NodeState(Struct):
    nombre: str= ""
    lado1: float= 0.0
    lado2: float= 0.0

arrayPuntos= []

@subscribe("datosCono", message_type= NodeState)
async def recibirDatos(msg= NodeState):
    puntoMedio= (msg.lado1+msg.lado2)/2
    arrayPuntos.append(puntoMedio)


