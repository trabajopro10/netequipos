function blinkColor() {
   var g = document.getElementById('idestado');
   var h = document.getElementById('idimagen');
   h.style.backgroundColor = "#01DF3A";
   setInterval(function() {
      g.style.color = (g.style.color == "orange") ? "green":"orange";
   }, 1000);
}

function blink() {
   var f = document.getElementById('idmensaje');
   f.style.color = (f.style.color == "red") ? "green":"red";
   setInterval(function() {
      f.style.display = (f.style.display == 'none' ? '' : 'none');
   }, 1000);
}

/*SE HACE ASÍ EN LINUX  */
function reload(url){
   setTimeout(function() { 
      window.location.href = url;
   },2000);
}

function msgalertaon(){
  document.getElementById("idmensaje").innerHTML =  " EQUIPOS CON PROBLEMAS ....";
  document.title = "!!HAY PROBLEMAS!!";
}

function msgalertaoff(){
   document.getElementById("idmensaje").innerHTML = " ";
   document.title = "OK_EQUIPOS";
}

function alertaoff(){
   alert("EQUIPO FUERA DE SERVICIO .... SOLUCIONAR ");
}

/* SE HACE  ASÍ EN WINDOWS  */
/*function reload(){
   setInterval(function() { 
      window.location.href = "http://172.16.1.51:8000/vnipconectequipos/";
   },6000);
}*/
function fnZoomScreen() {
    document.body.style.zoom = "65%";
}
