from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio
import pygame

class NodeState(Struct):
    nombre: str= ""
    x: float= 0.0
    y: float= 0.0

class NodeState2(Struct):
    x: float= 0.0
    ptoMedioY: float= 0.0

conosAzules= []
conosAmarillos= []
conosNaranjas= []
conosNaranjasGrandes= []
puntosTrazada= []


async def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1000, 700))
    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return

        dibujarTrazada(pantalla)

        pygame.display.flip()

        await asyncio.sleep(0.01) 
        reloj.tick(60)

def transformar(x, y):
    zoom= 8
    centroX= 500
    centroY= 350
    pX= int(x*zoom+centroX)
    pY= int(centroY-y*zoom)
    return(pX, pY)

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

@subscribe("Trazada",message_type= NodeState2)
async def leerTrazada(msg= NodeState2):
    puntosTrazada.append([msg.x, msg.ptoMedioY])

def dibujarTrazada(pantalla):
    pantalla.fill((30, 30, 30))
    for cono in conosAzules:
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (0,0,255), pos,3)
    for cono in conosAmarillos:
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (255,255,0), pos,3)
    for cono in conosNaranjas:
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (255,165,0), pos,3)
    for cono in conosNaranjasGrandes:
        pos= transformar(cono[0], cono[1])
        pygame.draw.circle(pantalla, (255,0,0), pos,3)
    
    if(len(puntosTrazada)>1):
        puntosTransformados= []
        for p in puntosTrazada:
            puntosTransformados.append(transformar(p[0],p[1]))
        pygame.draw.lines(pantalla,(255,255,255),False,puntosTransformados,2)

async def iniciar():
    asyncio.create_task(main())
    await start()

if __name__ == "__main__":
    asyncio.run(iniciar())