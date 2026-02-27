from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio

# Creo la clase cono para manejar los datos del csv acceleration
class Cono(Struct):
    nombre: str
    lado1: float
    lado2: float

# Creo la clase para introducir los datos de cada cono y publicarlo
class NodeState(Struct):
    nombre: str= ""
    lado1: float= 0.0
    lado2: float= 0.0

# Creo una función que abre el csv acceleration y va procesando línea a línea los datos, para irlos
# mandando por el topic llamado "datosConos". La función se ejecutará cada 0.2 segundos
@timer(0.2)
async def leerEnviarCsv():
    with open("csv/acceleration.csv", mode="r", encoding="utf-8") as csv:
        for linea in csv:
            linea= linea.strip()
            linea= linea.split(",")
            datosAEnviar= NodeState(nombre= linea[0], lado1= float(linea[1]), lado2= float(linea[2]))
            await publish("datosConos", datosAEnviar)
        datosAEnviar= NodeState(nombre= "FIN", lado1= 0, lado2= 0)
        await publish("datosConos", datosAEnviar)