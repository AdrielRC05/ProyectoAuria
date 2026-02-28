from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio

# Creo la clase cono para manejar los datos del csv acceleration
class Cono(Struct):
    nombre: str
    x: float
    y: float

# Creo la clase para introducir los datos de cada cono y publicarlo
class NodeState(Struct):
    nombre: str= ""
    x: float= 0.0
    y: float= 0.0

# Creo una función que abre el csv acceleration y va procesando línea a línea los datos, para irlos
# mandando por el topic llamado "datosConos". Podría añadir el @timer como dice el enunciado, pero como
# el csv es estático, lo dejo así

async def leerEnviarCsv():
    with open("csv/acceleration.csv", mode="r", encoding="utf-8") as csv:
        for linea in csv:
            linea= linea.strip()
            linea= linea.split(",")
            datosAEnviar= NodeState(nombre= linea[0], x= float(linea[1]), y= float(linea[2]))
            await publish("datosConos", datosAEnviar)
        datosAEnviar= NodeState(nombre= "FIN", x= 0, y= 0)
        await publish("datosConos", datosAEnviar)