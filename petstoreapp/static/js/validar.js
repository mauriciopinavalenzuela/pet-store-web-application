//FUNCIONES JS 

function validarFormulario() {
  //Obtener valores de los campos
  var rut = document.getElementById('rut');
  var nombre = document.getElementById('nom');
  var apellidoPaterno = document.getElementById('apeP');
  var apellidoMaterno = document.getElementById('apeM');
  var fechaNacimiento = document.getElementById('fecha');
  var edad = document.getElementById('edad');
  var genero = document.getElementById('genero');
  var rutmensaje = document.getElementById('rut-mensaje');
  var nombremensaje = document.getElementById('nom-mensaje');
  var apellidoPaternomensaje = document.getElementById('apeP-mensaje');
  var apellidoMaternomensaje = document.getElementById('apeM-mensaje');
  var fechaNacimientomensaje = document.getElementById('fecha-mensaje');
  var generomensaje = document.getElementById('genero-mensaje');
  var validacion = true;

  console.log(fechaNacimiento.value)

  // Validar que el Rut sea válido
  var esRutValido = validarRut(rut.value);

  if (!esRutValido) {
    rut.classList.add('input-error');
    rutmensaje.classList.remove('hide');
    validacion = false;
  } else {
    rut.classList.remove('input-error');
    rutmensaje.classList.add('hide');
  }

  // Validar que los campos nombre, apellidoPaterno y apellidoMaterno no estén vacíos
  if (nombre.value.trim() === '') {
    nombre.classList.add('input-error');
    nombremensaje.classList.remove('hide');
    validacion = false;
  } else {
    nombre.classList.remove('input-error');
    nombremensaje.classList.add('hide');
  }

  if (apellidoPaterno.value.trim() === '') {
    apellidoPaterno.classList.add('input-error');
    apellidoPaternomensaje.classList.remove('hide')
    validacion = false;
  } else {
    apellidoPaterno.classList.remove('input-error');
    apellidoPaternomensaje.classList.add('hide')
  }

  if (apellidoMaterno.value.trim() === '') {
    apellidoMaterno.classList.add('input-error');
    apellidoMaternomensaje.classList.remove('hide')
    validacion = false;
  } else {
    apellidoMaterno.classList.remove('input-error');
    apellidoMaternomensaje.classList.add('hide');
  }

  if (fechaNacimiento.value === '') {
    fechaNacimiento.classList.add('input-error');
    fechaNacimientomensaje.classList.remove('hide')
    validacion = false;
  } else {
    fechaNacimiento.classList.remove('input-error');
    fechaNacimientomensaje.classList.add('hide');
  }

  // Validar que se haya seleccionado un género
  if (genero.value === '0') {
    genero.classList.add('input-error');
    generomensaje.classList.remove('hide');
    validacion = false;
  } else {
    genero.classList.remove('input-error');
    generomensaje.classList.add('hide')
  }
  // Si se llega hasta aquí, el formulario es válido
  return validacion;
}

// Función para validar el RUT
function validarRut(rut) {
  if (!/^[0-9]+[-‐]?[0-9kK]{1}$/.test(rut)) {
    return false;
  }
  var tmp = rut.split('-');
  var digv = tmp[1];
  var rut = tmp[0];
  if (digv === 'K') digv = 'k';
  return (dv(rut) == digv);
}

function dv(T) {
  var M = 0, S = 1;
  for (; T; T = Math.floor(T / 10))
    S = (S + T % 10 * (9 - M++ % 6)) % 11;
  return S ? S - 1 : 'k';
}

function upperText(input) {
  input.value = input.value.toUpperCase();
}