const cantCuotas = document.querySelector("#id_cantCuotas");
const montoAPagar = document.querySelector("#montoCuota");
const log = document.getElementById("etiqueta");

console.log(log);
cantCuotas.addEventListener("input", updateValue);

function updateValue(e) {
    console.log (montoAPagar.value)
  log.textContent = montoAPagar.value*e.srcElement.value;
}