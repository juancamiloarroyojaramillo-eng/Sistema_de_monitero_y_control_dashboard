# Sistema de Monitoreo Ambiental con ESP32 y Dashboard Web
## Descripción del trabajo
Este proyecto implementa un sistema de monitoreo ambiental basado en una ESP32 programada en MicroPython y una interfaz web para visualización de variables en tiempo real.

El sistema realiza la lectura de:
* **Temperatura ambiental** mediante un sensor LM35.
* **Nivel de iluminación** mediante un sensor LDR.
* **Temperatura de referencia** ajustable mediante un potenciómetro.

Con base en estas variables:
* Se controla un servomotor, que cambia de posición dependiendo de si la temperatura medida supera la temperatura de referencia.
* Se activa uno de tres LEDs indicadores según el nivel de iluminación detectado.
* La ESP32 funciona como servidor web y envía las variables en tiempo real al dashboard web mediante solicitudes HTTP, permitiendo visualizar dinámicamente el estado del sistema.

La interfaz web permite visualizar:
* Temperatura medida
* Temperatura de referencia
* Nivel de luz
* Estado del sistema
* Estado del servomotor
* LED activo
* Gráfica dinámica de temperatura

## Pines usados en la ESP32

### Sensores de entrada
| Dispositivo                | Pin ESP32 |
| -------------------------- | --------: |
| LM35                       |   GPIO 34 |
| LDR                        |   GPIO 35 |
| Potenciómetro              |   GPIO 32 |
| Botón de encendido/apagado |   GPIO 22 |

### Actuadores de salida
| Dispositivo  | Pin ESP32 |
| ------------ | --------: |
| LED rojo     |   GPIO 12 |
| LED amarillo |   GPIO 14 |
| LED verde    |   GPIO 27 |
| Servomotor   |   GPIO 26 |


## Dashboard Web

El dashboard web fue desarrollado para representar gráficamente el estado lógico del sistema y mostrar en tiempo real las variables enviadas por la ESP32.

La interfaz muestra:
* **Temperatura medida:** valor leído desde el sensor LM35.
* **Temperatura de referencia:** valor ajustado por el potenciómetro.
* **Nivel de luz:** clasificación baja, media o alta.
* **Estado del sistema:** activo o inactivo.
* **Estado del servomotor:** abierto o cerrado.
* **LED activo:** rojo, amarillo o verde.
* **Gráfica de barras:** evolución de la temperatura en tiempo real.

Además, las tarjetas del dashboard cambian de color según el estado del sistema, el estado del servomotor y el LED activo para mejorar la visualización del monitoreo.


### Archivos del dashboard
* `index.html` → estructura principal de la interfaz web.
* `style.css` → estilos visuales del dashboard.
* `datos.js` → actualización dinámica de datos y control visual del dashboard.
* `main.py` → lógica principal del sistema en la ESP32, adquisición de datos y servidor web.


## Instrucciones de operación

### 1. Configuración del sistema
1. Conectar los sensores y actuadores a la ESP32 según la tabla de pines.
2. Cargar el archivo `main.py` en la ESP32 usando MicroPython.
3. Configurar la red WiFi en el código principal.
4. Ejecutar el sistema para iniciar la lectura de sensores y el servidor web embebido.
5. La ESP32 generará una dirección IP local para acceder a los datos del sistema.

### 2. Ejecución del dashboard web
1. Abrir la carpeta del dashboard en Visual Studio Code.
2. Ejecutar el archivo `index.html` usando **Live Server**.
3. El archivo `datos.js` realiza solicitudes HTTP a la ESP32 para consultar las variables en tiempo real.
4. La página web actualizará automáticamente las variables y la gráfica dinámica del sistema.

### 3. Lógica de operación
* Si la temperatura medida es menor que la referencia:
  * el servomotor permanece cerrado.
* Si la temperatura medida es mayor o igual a la referencia:
  * el servomotor se abre a 90°.

Según la lectura del sensor LDR:
* Si la luz es baja:
  * se activa el LED rojo.
* Si la luz es media:
  * se activa el LED amarillo.
* Si la luz es alta:
  * se activa el LED verde.

## Tecnologías utilizadas

* **MicroPython** para la lógica embebida en ESP32.
* **HTML** para la estructura del dashboard.
* **CSS** para la interfaz visual.
* **JavaScript** para la actualización dinámica de datos.
* **HTTP** para la comunicación entre la ESP32 y la interfaz web.

## Resultado esperado
El sistema permite supervisar variables ambientales y visualizar el estado operativo en una interfaz web amigable y dinámica, integrando sensores, actuadores y monitoreo en tiempo real mediante comunicación entre la ESP32 y el dashboard web.
