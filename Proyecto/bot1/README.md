# bots_INTEGRO

## ChatScript
Esta imagen de Docker está realizada con ChatScript [11.5](https://github.com/ChatScript/ChatScript/releases/tag/11.5).
Lo primero que hay que hacer es construir la imagen de docker de chatscript que se usará como base para poner los bots:

```
docker build -t chatscript-base .
docker run chatscript-base
```

## Instrucciones

Luego de clonar el repositorio y entrar en la carpeta de chatscript es necesario seguir los siguientes pasos.

Primero se debe establecer la carpeta del bot, la cual puede ser editada desde la plantilla del bot que viene de ejemplo, o reemplazando esta por una carpeta con un bot ya escrito en código.

<img src="images/1.png"></img>

Luego en Dockerfile deben estar las variables de ambiente correspondientes a __nombre del bot__ y __puerto__.
Recordar que el nombre del bot debe ser exactamente el mismo que el nombre de la carpeta de este.

<img src="images/2.png"></img>

En docker-compose.yml se debe definir el __nombre del servicio__, el cual puede ser algo relacionado con el cliente o bot, el __nombre del contenedor__ y los __puertos__ a ocupar.

<img src="images/3.png"></img>

Por último compilar el contenedor con el siguiente comando.

```
docker-compose up -d --build
```

<img src="images/4.png"></img>
 
Ejecutando una lista de los contenedores se puede apreciar el contenedor funcionando.

```
docker ps
```

<img src="images/5.png"></img>


## Envío de mensajes

El mismo script de healthcheck se puede utilizar para enviar mensajes al bot y obtener su respuesta. El formato es:

```perl
perl healthcheck.pl <mensaje> <usuario> --botname bot_template --port 1050
```

al ir cambiando el mensaje se puede conversar con el bot.

## Ingresar al contenedor

Si se desea ingresar al contenedor para envío de mensajes:

```
docker exec -it bot_TEMPLATE bash
```

<img src="images/6.png"></img>

Y luego, haciendo conexión con el servidor de chatscript en el puerto especificado utilizando el cliente de chatscript, sockets o similares, se puede interactuar con el bot.

<img src="images/7.png"></img>


Según la compilación desde la línea de comandos usada para este contenedor, los parámetros necesarios solo son __usuario__ y __mensaje__, por lo que añadir el nombre del bot podría ocasionar errores.

Un ejemplo de envío de mensajes es el siguiente.

```
s.sendall(str.encode("test" + chr(0) + "" + chr(0) + "mensaje AQUÍ" + chr(0)))
```
