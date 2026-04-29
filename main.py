# =========================
# IMPORTACIÓN DE LIBRERÍAS
# =========================
from machine import Pin, ADC, PWM # type: ignore
from utime import sleep, ticks_ms, ticks_diff # type: ignore
import network # type: ignore
import socket
import ujson # type: ignore

# =========================
# WIFI
# =========================
ssid = "paul"
password = "123456789"
# =========================
# WIFI (VERSIÓN ROBUSTA)
# =========================
ssid = "iPhone de Sara Camila"       
password = "1013337155"

wifi = network.WLAN(network.STA_IF)
wifi.active(False)  
sleep(0.5)          
wifi.active(True)   

print("Intentando conectar a:", ssid)
wifi.connect(ssid, password)

# Intentamos conectar por máximo 15 segundos para no bloquear el programa
intentos = 0
while not wifi.isconnected() and intentos < 15:
    sleep(1)
    intentos += 1
    print(f"Intento {intentos}...")

if wifi.isconnected():
    print("\n¡CONECTADO!")
    print("Configuración de red:", wifi.ifconfig())
    print("IP para el dashboard:", wifi.ifconfig()[0])
else:
    print("\n[!] No se pudo conectar al WiFi.")
    print("El sistema físico funcionará, pero el dashboard no tendrá datos.")
    # No usamos 'continue' ni bloqueamos, para que el código siga a los pines

# =========================
# CONFIGURACIÓN DE PINES
# =========================
led_rojo = Pin(12, Pin.OUT)
led_amarillo = Pin(14, Pin.OUT)
led_verde = Pin(27, Pin.OUT)
boton = Pin(22, Pin.IN, Pin.PULL_UP)

lm35 = ADC(Pin(34))
ldr = ADC(Pin(35))
pot = ADC(Pin(32))

lm35.atten(ADC.ATTN_11DB)
ldr.atten(ADC.ATTN_11DB)
pot.atten(ADC.ATTN_11DB)

servo = PWM(Pin(26), freq=50)

# =========================
# VARIABLES DE CONTROL
# =========================
bandera_sistema = False
ultimo_tiempo = 0
# Diccionario global para que el servidor siempre tenga algo que enviar
datos_actuales = {
    "temperatura": 0,
    "referencia": 0,
    "luz": "N/A",
    "estado": "DESACTIVADO",
    "servo": "0°",
    "led": "Ninguno"
}

# =========================
# FUNCIONES
# =========================
def set_servo(angle): 
    duty = int((angle / 90) * (77 - 26) + 26)
    servo.duty(duty)

def apagar_todo(): 
    led_rojo.value(0)
    led_amarillo.value(0)
    led_verde.value(0)
    set_servo(0)

def toggle_sistema(pin):
    global bandera_sistema, ultimo_tiempo
    ahora = ticks_ms()
    if ticks_diff(ahora, ultimo_tiempo) > 300:
        bandera_sistema = not bandera_sistema
        print("Sistema ACTIVADO" if bandera_sistema else "Sistema DESACTIVADO")
        ultimo_tiempo = ahora

# =================================
# INICIALIZACIÓN DEL SERVIDOR WEB
# =================================
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(1)
server.settimeout(0.05) # Timeout muy corto para no frenar el loop de sensores
print("Servidor activo en la IP del ESP")

# =========================
# INTERRUPCIÓN
# =========================
boton.irq(trigger=Pin.IRQ_FALLING, handler=toggle_sistema)

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    # --- 1. ATENDER PETICIONES DEL DASHBOARD ---
    try:
        client, addr_client = server.accept()
        request = client.recv(1024).decode()
        
        # Si piden la ruta de datos
        if "/datos" in request:
            response = ujson.dumps(datos_actuales)
            # Encabezados HTTP con CORS habilitado
            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: application/json\r\n")
            client.send("Access-Control-Allow-Origin: *\r\n") # Esto quita el error de datos.js
            client.send("Connection: close\r\n")
            client.send("\r\n")
            client.send(response)
        
        # Opcional: Servir el index.html si no usas Live Server
        elif "GET / " in request:
            with open("index.html", "r") as f:
                html = f.read()
            client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            client.send(html)

        client.close()
    except Exception:
        # El timeout del socket genera una excepción cuando nadie se conecta, 
        # simplemente la ignoramos para seguir con la lectura de sensores
        pass

    # --- 2. CONTROL DEL SISTEMA FÍSICO ---
    if not bandera_sistema:
        apagar_todo()
        datos_actuales["estado"] = "DESACTIVADO"
        sleep(0.1)
        continue

    # --- 3. LECTURAS (Tus fórmulas originales) ---
    # Temperatura
    valor_temp = lm35.read()
    voltaje = (valor_temp / 4095) * 3.3
    temperatura = voltaje * 100

    # Potenciómetro (Referencia)
    valor_pot = pot.read()
    temp_ref = 25 + (valor_pot / 4095) * (45 - 25)

    # Control Servo
    if temperatura < temp_ref:
        set_servo(0)
        set_estado = "0° (cerrado)"
    else:
        set_servo(90)
        set_estado = "90° (abierto)"

    # Sensor de Luz
    valor_luz = ldr.read()
    led_rojo.value(0)
    led_amarillo.value(0)
    led_verde.value(0)

    if valor_luz < 1000:
        led_rojo.value(1)
        luz_desc = "Baja"
        led_desc = "Rojo"
    elif valor_luz < 2500:
        led_amarillo.value(1)
        luz_desc = "Media"
        led_desc = "Amarillo"
    else:
        led_verde.value(1)
        luz_desc = "Alta"
        led_desc = "Verde"

    # --- 4. ACTUALIZAR DICCIONARIO PARA EL DASHBOARD ---
    datos_actuales = {
        "temperatura": round(temperatura, 2),
        "referencia": round(temp_ref, 2),
        "luz": luz_desc,
        "estado": "ACTIVO",
        "servo": set_estado,
        "led": led_desc
    }
    
    # Un pequeño respiro para el procesador
    sleep(0.05)