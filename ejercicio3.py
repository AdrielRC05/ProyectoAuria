from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio
import pygame


# Para que funcione, debes ejecutar en terminales distintas en el siguiente orden:
# ejercicio3.py
# ejercicio2.py
# ejercicio1.py


class NodeState(Struct):
    nombre: str= ""
    x: float= 0.0
    y: float= 0.0

class NodeState2(Struct):
    ptoMedioX: float= 0.0
    ptoMedioY: float= 0.0

conosAzules= []
conosAmarillos= []
conosNaranjas= []
conosNaranjasGrandes= []
puntosTrazada= []

# Esta función arranca el programa. Inicializa pygame, la pantalla, la pinta de negro,
# llama a la función para dibujar la trazada y los conos, el flip muestra las cosas por
# pantalla y el await asyncio es para que no consuma toda la cpu del ordenador
async def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1000, 700))
    while True:
        pantalla.fill((0,0,0))
        dibujarTrazada(pantalla)
        pygame.display.flip()
        await asyncio.sleep(0.01)

# Esto permite dibujar bien la parte gráfica, para que tenga buen tamaño y se vea centrado
def transformar(x, y):
    return (int(x*8+500), int(350-y*8))

# Esta función lee los datos del primer topic y separa los datos de los conos por colores
@subscribe("datosConos",message_type= NodeState)
async def leerConos(msg= NodeState):
    if(msg.nombre=="blue"):
        conosAzules.append([msg.x, msg.y])
    if(msg.nombre=="yellow"):
        conosAmarillos.append([msg.x, msg.y])
    if(msg.nombre=="orange"):
        conosNaranjas.append([msg.x, msg.y])
    if(msg.nombre=="big_orange"):
        conosNaranjasGrandes.append([msg.x, msg.y])

# Esta función lee el segundo topic y guarda los datos de la trazada
@subscribe("Trazada",message_type= NodeState2)
async def leerTrazada(msg= NodeState2):
    puntosTrazada.append([msg.ptoMedioX, msg.ptoMedioY])

# Esta función dibuja los conos y la trazada
def dibujarTrazada(pantalla):
    for cono in conosAzules:
        # Pinta los conos azules de azul
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (0,0,255), pos,3)
    for cono in conosAmarillos:
        # Pinta los conos amarillos de amarillo
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (255,255,0), pos,3)
    for cono in conosNaranjas:
        # Pinta los conos naranjas de naranja
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (255,165,0), pos,3)
    for cono in conosNaranjasGrandes:
        # Pinta los conos naranjas grandes de rojo
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (255,0,0), pos,3)
    
    # Siempre que haya más de una coordenada en el array (lo mínimo para dibujar una línea son 2 puntos),
    # dibujará una línea blanca uniendo los puntos medios que tiene el array
    if(len(puntosTrazada)>1):
        puntosTransformados= []
        for p in puntosTrazada:
            puntosTransformados.append(transformar(p[0],p[1]))
        pygame.draw.lines(pantalla,(255,255,255),True,puntosTransformados,2)

# Esto inicia el programa y hace que ni entre en deadlocks ni haga esperar al resto de programas
async def iniciar():
    asyncio.create_task(main())
    await start()

if __name__ == "__main__":
    asyncio.run(iniciar())

# Para que funcione, debes ejecutar en terminales distintas en el siguiente orden:
# ejercicio3.py
# ejercicio2.py
# ejercicio1.py
