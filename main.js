const   url='http://127.0.0.1:8000/',
        btnEnviarIp = document.getElementById("btnEnviar"),
        btnSubirGra = document.getElementById("btnSubirGra"),
        ipEnviar = document.getElementById("ip"),
        comunidad = document.getElementById("comunidad"),
        mensaje1 = document.getElementById("alerta1"),
        mensaje2 = document.getElementById("alerta2"),
        titulo1 = document.getElementById("titulo1"),
        titulo2 = document.getElementById("titulo2");

var     traficIn=new Array,
        traficOut=new Array,
        ctx = document.getElementById('myChart').getContext('2d'),
        ctx2 = document.getElementById('myChart2').getContext('2d'),
        tituloIn="MB tráfico de entrada",
        tituloOut="MB tráfico salida"
        colorAzul="rgba(54, 162, 235, 0.8)",
        colorRojo="rgba(255, 99, 132, 0.8)";
        

//funcion que imprime las ips disponibles
function imprimirIps(ips) {
    for (var i = 0; i < ips.length; i++){
        document.getElementById("pruebaIps").insertRow(-1).innerHTML = '<td>'+ips[i]+'</td>';
    }
    mensaje2.style.display = "none";
}//fin de imprimirIps

//funcion que crea los arreglos del ancho de banda utilizado para despues ser graficado
function creaTra(data,j) {
    for (let i = 0; i < 5; i++) {
        if (j==0) {
            traficIn.push(data[i][j]);    
        }else{
            traficOut.push(data[i][j])
        }          
    }
}//fin de creaTra

//funcion que grafica el anco de banda de entrada y salida
function crearGra(grafica,titulo,vector,color,borde) {
    var myChart = new Chart(grafica, {
            type: 'bar',
            data: {
                labels: ['5 sec', '10 sec', '15 sec', '20 sec', '25 sec'],
                datasets: [{
                    label: titulo,
                    data: vector,
                    backgroundColor: [
                            color,
                            color,
                            color,
                            color,
                            color
                        ],
                    borderColor: [
                            borde,
                            borde,
                            borde,
                            borde,
                            borde
                        ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
}//fin de crearGra

//Events listeners
btnEnviarIp.addEventListener("click", () => {
    mensaje1.style.display = "block";
    var dataSend=new FormData();
    dataSend.append('comunidad',comunidad.value);
    dataSend.append('ip',ipEnviar.value);
    //obtiene el ancho de banda
    getDatos(dataSend);
    getAncho(dataSend);
}); //fin de btnEnviarIp

btnSubirGra.addEventListener("click", () => {
    var canvas = document.getElementById("myChart");
    canvas.toBlob(function(blob) {
        const formData = new FormData();
        formData.append('file', blob, 'grafica.png');
        subir(formData);
    });

    var canvas2 = document.getElementById("myChart2");
    canvas2.toBlob(function(blob) {
        const formData = new FormData();
        formData.append('file', blob, 'grafica2.png');
        subir(formData);
    });   
});//fin de btnSubirGra

/*
*****************
PETICIONES GET  *
*****************
*/
 
//funcion asincrona que obtiene las ips disponibles en la red
async function getIps() {
    await fetch(url+'getIps')
        .then(response=> {
            return response.json();
        })
        .then(data=> {
            imprimirIps(data)
        })
        .catch(err=> {
            console.error(err);
        });
}//fin de getIps

/*
****************
PETICIONES POST*
****************
*/
//funcion que obtiene el ancho de banda utilizado 
async function getAncho(dataSend) {
    await fetch(url+'getAncho', {
        method: 'POST',
        body: dataSend
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        creaTra(data,0);
        creaTra(data,1);
        mensaje1.style.display = "none";
        titulo2.style.display = "block";
        crearGra(ctx,tituloIn,traficIn,colorAzul,colorRojo);
        crearGra(ctx2,tituloOut,traficOut,colorRojo,colorAzul);
        btnSubirGra.style.display = "block";
    })
    .catch(function(err) {
        console.error(err);
    });
}//fin de getAncho

//funcion que obtiene la informacion SNMP de un dispositivo
async function getDatos(dataSend) {
    await fetch(url+'getDatos', {
        method: 'POST',
        body: dataSend
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(datos) {
        titulo1.style.display = "block";
        if (datos.hasOwnProperty('data')){
            var node = document.createTextNode(datos.data);
            titulo1.appendChild(node);
        }
    })
    .catch(function(err) {
        console.error(err);
    });
}//fin de getDatos

//funcion para subir la imagen al servidor de la grafica
async function subir(dataSend) {
    await fetch(url+'upload', {
        headers:{
            'Access-Control-Allow-Origin':'*'
        },
        method: 'POST',
        body: dataSend
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.hasOwnProperty('ok')){
            if (data.ok==='true') {
                alert('Se guardo la grafica correctamente');
            }else{
                alert(data.message);
            }
        }
    })
    .catch(function(err) {
        console.error(err);
    });
}//fin de subir



