from msgspec import Struct
from starting_pack import encoder, subscribe, timer, publish, start
import asyncio

# La arquitectura productor/subscriptor se basa en enviar mensajes por canales y recibir los mensajes que se envian por cada canal
# para enviar mensajes se usa publish, para recibirlos se usa @subscribe como decorador de una función. Los canales también se llaman
# topics, se definen por su nombre, una cadena.
# Este programa de ejemplo enseña como definir los mensajes que se usan, como enviarlos por canales y como subscribirse a esos canales


# así se definen los mensajes que se envian por los topics, lo más cómodo
# es definirlos en un archivo aparte para poder compartir las mismas definiciones entre varios programas
# hay que especificar el tipo de los datos obligatoriamente con anotaciones de tipos de python

class TipoMensaje(Struct):
	dato1 : str
	
	
# para crear mensajes lo hacemos como cualquier otra clase
# mensaje_nuevo = TipoMensaje(dato1=1,dato2=2.2,dato3="asd",dato4=[])

# El estado lo guardamos en su propia clase
class NodeState(Struct):
	variable1 : str=""

# Creamos una instancia de esa clase
state = NodeState()

# para crear una subscripcion  a un topic se usa @subscribe, en este ejemplo
# cada vez que llega un mensaje al topic "topic" se ejecuta subscriber_callback con ese mensaje,
# adicionalmente le indicamos que el mensaje es de tipo "TipoMensaje"
 
@subscribe("topic",TipoMensaje)
async def subscriber_callback(msg : TipoMensaje):
	print(msg.dato1)
	
# @timer ejecuta algo periodicamente, en este caso "timer_callback" se ejecutará 10 veces por segundo 
@timer(0.5)
async def timer_callback():
	nuevo_mensaje= TipoMensaje(dato1= "Hola @subscriber")
	await publish("topic",nuevo_mensaje)
	print(f"Hola @timer")

# IMPORTANTE: todas las funciones que tengan decoradores (@subscribe y @timer) deben ser async
# y cuando publiqueis mensajes con publish teneis que hacer `await publish(...)`
# NO teneis que preocuparos de nada más con respecto a cosas asíncronas que esas dos cosas


# así se inicializan los programas que usan el starting_pack
if __name__ == "__main__":
	asyncio.run(start())

# para aseguraros de que entendeis el ejemplo, intentad publicar y recibir mensajes periodicamente, por ejemplo podéis
# modificar la función `timer_callback` para que envíe mensajes y que `subscriber_callback` los reciba