let temperaturas = [];
let etiquetas = [];

const ctx = document.getElementById("graficaTemp").getContext("2d");

const grafica = new Chart(ctx, {
    type: "bar",
    data: {
        labels: etiquetas,
        datasets: [{
            label: "Temperatura °C",
            data: temperaturas,
            backgroundColor: "#4dabf7"
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 50 // Sugerido: escala fija para que la gráfica no salte mucho
            }
        }
    }
});

function actualizarDatos() {
    // 1. Cambia esta IP por la que salga en el monitor serial de Thonny/VSCode
    fetch("http://172.20.10.2/datos")
    .then(response => {
        if (!response.ok) throw new Error("Error en respuesta");
        return response.json();
    })
    .then(datos => {
        // Actualización de textos
        document.getElementById("temp").innerText = datos.temperatura + " °C";
        document.getElementById("ref").innerText = datos.referencia + " °C";
        document.getElementById("luz").innerText = datos.luz;
        document.getElementById("estado").innerText = datos.estado;
        document.getElementById("servo").innerText = datos.servo;
        document.getElementById("led").innerText = datos.led;

        // CARD ESTADO
        // Usamos .toUpperCase() para evitar errores de mayúsculas/minúsculas
        if(datos.estado.toUpperCase() === "ACTIVO"){
            document.getElementById("card-estado").style.backgroundColor = "#d9f2ff"; 
        } else {
            document.getElementById("card-estado").style.backgroundColor = "#ffe8cc";
        }

        // CARD SERVO (Corregido para detectar "abierto" o "ABIERTO")
        if(datos.servo.toUpperCase().includes("ABIERTO")){
            document.getElementById("card-servo").style.backgroundColor = "#dbeafe";
        } else {
            document.getElementById("card-servo").style.backgroundColor = "#f1f3f5";
        }

        // CARD LED
        let colorLed = "gray";
        let colorCard = "white";

        if(datos.led === "Rojo"){
            colorLed = "red";
            colorCard = "#ffe5e5";
        }
        else if(datos.led === "Amarillo"){
            colorLed = "gold";
            colorCard = "#fff9db";
        }
        else if(datos.led === "Verde"){
            colorLed = "green";
            colorCard = "#e6ffed";
        }

        document.getElementById("led-indicador").style.backgroundColor = colorLed;
        document.getElementById("card-led").style.backgroundColor = colorCard;

        // GRÁFICA
        temperaturas.push(datos.temperatura);
        etiquetas.push(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));

        if(temperaturas.length > 8){
            temperaturas.shift();
            etiquetas.shift();
        }

        grafica.update();
    })
    .catch(error => {
        console.warn("Esperando al ESP32... ", error);
        document.getElementById("estado").innerText = "DESCONECTADO";
        document.getElementById("card-estado").style.backgroundColor = "#ffc9c9";
    });
}

// 5000ms (5 seg) es perfecto para no saturar al ESP32
setInterval(actualizarDatos, 5000);
actualizarDatos();