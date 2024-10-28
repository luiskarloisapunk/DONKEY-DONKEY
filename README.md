# DONKEY DONKEY!

¿Cansado de renombrar tus archivos para el portafolio digital manualmente?,
***¡Enhorabuena que El Burro está aquí!***, presentando a Donkey Donkey!, una herramienta que permite a los estudiandos de la carrera de programación automatizar el nombramiento de archivos en el portafolio digital solicitado por Jorge Ibarra.

## Requerimientos
1. Python 3.10
2. Modulos indicados en el *requirements.txt*

[========]


## Funcionamiento
El Burro pide tu nombre completo (escrito por apellidos como se indica en el manual de documentación), tu número de control a 14 digitos, tu grupo y el tipo de operación que va a realizar: *"Renombrar Proyectos"* ó *"Renombrar Conceptos & Resumenes"*

###Proyectos
Pregunta el número de proyecto que va a documentar y a continuación pide la dirección de la carpeta donde se encuentran los archivos del proyecto antes señalado, después El Burro analiza los archivos dentro de la carpeta para determinar si se trata de proyectos con .html o no y a continuación aplica un clasificador de imagenes *keras* entrenado para distinguir entre vistas de navegador, código y hojas de libreta y las renombra de acuerdo al manual:
*Archivos -> Código -> Vista de navegador -> Libreta*

- ####Proyectos con .html
 Recuerda anidar el numero de documento de los .html (ubicado en el bloque  identificador exigido) en la clase ***"id"***.

###Conceptos & Resumenes
Pide la dirección de la carpeta donde se tienen las fotos de todos los conceptos y resumenes, a continuación El Burro edita momentaneamente las imagenes con el  fin de hacerlas más legibles para el OCR, después aplica correciones a errores comúnes cometidos por el OCR, extrae el tipo de trabajo, número de trabajo y número de página, y finalmente nombra los archivos de acuerdo a la nomenclatura del manual. 

[========]

## Tips
- Instalar [Python 3.10.x](https://www.python.org/downloads/release/python-31011/ "Python 3.10.x").

- Se recomienda instalar [Visual Studio Code](https://code.visualstudio.com/download "Visual Studio Code") para su ejecución, más es opcional.

- Para instalar la carpeta del repositorio puedes dirigirte a [este link](https://download-directory.github.io/ "este link") y pegar la dirección del repositorio ( *https://github.com/luiskarloisapunk/DONKEY-DONKEY.git* )

- Para instalar los modulos ejecuta `pip install -r requirements.txt` en la dirección de la carpeta (terminal)
