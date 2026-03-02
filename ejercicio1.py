from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio


# Para que funcione, debes ejecutar en terminales distintas en el siguiente orden:
# ejercicio3.py
# ejercicio2.py
# ejercicio1.py


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

# Creo una función que abre el csv seleccionado y va procesando línea a línea los datos, para irlos
# mandando por el topic llamado "datosConos". Podría añadir el @timer como dice el enunciado, pero como
# los csv son estáticos, lo dejo así

async def leerEnviarCsv():

    #Esta pausa es para que no entre en deadlock
    await asyncio.sleep(1)
    csvElegido= input("Escribe el nombre del csv que quieres procesar (con la extensión): ")

    with open(f"csv/{csvElegido}", mode="r", encoding="utf-8") as csv:
        for linea in csv:
            linea= linea.strip()
            linea= linea.split(",")
            if(len(linea)>2 and linea[0]!="tag" and linea[1]!="x" and linea[2]!="y"):
                datosAEnviar= NodeState(nombre= linea[0], x= float(linea[1]), y= float(linea[2]))
                await publish("datosConos", datosAEnviar)
        datosAEnviar= NodeState(nombre= "FIN", x= 0, y= 0)
        await publish("datosConos", datosAEnviar)

# Esto lo pongo para evitar un posible deadlock
async def iniciar():
    asyncio.create_task(leerEnviarCsv())
    await start()

if __name__ == "__main__":
    asyncio.run(iniciar())

# Para que funcione, debes ejecutar en terminales distintas en el siguiente orden:
# ejercicio3.py
# ejercicio2.py
# ejercicio1.py
