var mdcAssignedVars = {};

function init(){
    swcms.mdcSelects.forEach((sel) => {
    if (sel.assignedVar)
        mdcAssignedVars[sel.assignedVar] = sel;
    });
    fetch("/static/js/datahn.json")
    .then(response => response.json())
    .then(data => {
        console.log(data); // Aquí puedes manipular los datos del JSON
        setDepartamentos(data) ;
        console.log(data)
        console.log('Fin de llamada de datos')
    })
    .catch(error => console.error("Error al cargar el archivo JSON:", error));


}


function crearNuevaOpcion(value, text) {

    // Crear un nuevo elemento de lista
    const newListItem = document.createElement('li');
    newListItem.classList.add('mdc-deprecated-list-item');
    newListItem.classList.add('mdc-ripple-upgraded');
    newListItem.setAttribute('aria-selected', 'false');
    newListItem.setAttribute('data-value',value);
    //newListItem.setAttribute('aria-disabled', 'true');
    newListItem.setAttribute('role', 'option');

    // Crear elementos de texto para la nueva opción de la lista
    const rippleSpan = document.createElement('span');
    rippleSpan.classList.add('mdc-deprecated-list-item__ripple');

    const textSpan = document.createElement('span');
    textSpan.classList.add('mdc-deprecated-list-item__text');
    textSpan.textContent = text;

    // Agregar los elementos de texto al nuevo elemento de lista
    newListItem.appendChild(rippleSpan);
    newListItem.appendChild(textSpan);

    // Agregar un evento clic a la nueva opción
    newListItem.addEventListener('click', function() {
        // Aquí puedes agregar la lógica que desees cuando se haga clic en la nueva opción
        console.log('Hiciste clic en la opción:', value);
    });
    return newListItem;
}



  //iniciar el selec departamentos
function setDepartamentos(respuesta){

      if(respuesta.estado==1){
          departamentos=respuesta.departamentos
          municipios=respuesta.municipios
          aldeas=respuesta.aldeas

          hp = ``
          // Obtener el contenedor de la lista
          var listContainer = document.querySelector('#list-depto');
          listContainer.innerHTML = ''

          // Ordena el arreglo de departamentos por el código
          departamentos= departamentos.sort((a, b) => {
              // Compara los códigos de los departamentos
              return a.codigo.localeCompare(b.codigo);
          });
          listContainer.appendChild(crearNuevaOpcion('', ''))
          console.log(departamentos); // Muestra el arreglo de departamentos ordenado por código
          for (let i in departamentos) {
              // Ahora puedes agregar la nueva opción al contenedor de la lista
              const nuevaOpcion = crearNuevaOpcion(departamentos[i].id, departamentos[i].nombre);
              // Agregar el nuevo elemento de lista al contenedor de la lista
              listContainer.appendChild(nuevaOpcion);
          }

          
          mdcAssignedVars['txt_departamento'].layoutOptions();

      }else{
          console.log(respuesta)
      }
}


//funciones lugar de nacimiento
function nacDepto(ff){

  console.log(mdcAssignedVars['txt_departamento'].value)
  var listContainer = document.querySelector('#list-muni');
  listContainer.innerHTML = ''
  listContainer.appendChild(crearNuevaOpcion('', ''))
  for (let i in municipios) {
      if(ff==municipios[i].iddepartamento__id){
              // Ahora puedes agregar la nueva opción al contenedor de la lista
            const nuevaOpcion = crearNuevaOpcion(municipios[i].id, municipios[i].nombre);
              // Agregar el nuevo elemento de lista al contenedor de la lista
            listContainer.appendChild(nuevaOpcion);
          }
      }
      mdcAssignedVars['txt_municipio'].layoutOptions();
      mdcAssignedVars['txt_municipio'].selectedIndex = -1;

      listContainer = document.querySelector('#list-aldea');
      listContainer.innerHTML = ''
      mdcAssignedVars['txt_aldea'].selectedIndex = -1;
  }

function nacMum(ff){
  console.log(ff)
  var listContainer = document.querySelector('#list-aldea');
  listContainer.innerHTML = ''
  listContainer.appendChild(crearNuevaOpcion('', ''))
  for (let i in aldeas) {
      if(ff==aldeas[i].idmunicipio__id){
        // Ahora puedes agregar la nueva opción al contenedor de la lista
        const nuevaOpcion = crearNuevaOpcion(aldeas[i].id, aldeas[i].nombre);
        // Agregar el nuevo elemento de lista al contenedor de la lista
        listContainer.appendChild(nuevaOpcion);
      }
  }
  mdcAssignedVars['txt_aldea'].layoutOptions();
  mdcAssignedVars['txt_aldea'].selectedIndex = -1;
}

// Obtiene el botón por su ID
const submitButton = document.getElementById('submitSaveButton');

// Agrega un listener para el evento 'click'
submitButton.addEventListener('click', function() {
    // Acciones a realizar cuando se hace clic en el botón
    console.log('¡El botón fue clickead2o!');
    
    // Asignación de elementos a mdcAssignedVars
    let preguntas = []
    const Swal = swcms.returnSwal()
    swcms.mdcSelects.forEach((sel) => {
      if (sel.assignedVar)
          mdcAssignedVars[sel.assignedVar] = sel;
    });
    swcms.mdcTextInputs.forEach((txt) => {
      if (txt.assignedVar)
          mdcAssignedVars[txt.assignedVar] = txt;
    });

    swcms.mdcCheckbox.forEach((sel) => {
        if (sel.assignedVar)
            mdcAssignedVars[sel.assignedVar] = sel;
    })

      var respuesta ;
      var respuestas = [];
      // Obtener todos los elementos input con la clase mdc-text-field__input
      var inputs = document.querySelectorAll('.mdc-text-field__input');
      
      // Iterar sobre los elementos input
      for (var i = 0; i < inputs.length; i++) {
          var input = inputs[i];
          // Obtener el atributo hiddenlabel del elemento padre
          var hiddenLabel = input.parentElement.querySelector('.mdc-floating-label').getAttribute('hiddenlabel');
          var idLabel = input.parentElement.querySelector('.mdc-floating-label').getAttribute('id');
          // Verificar si el valor del input está en blanco
          if (input.value.trim() === '') {
              // Mostrar un mensaje alert con la pregunta que hace falta
              //alert('Por favor, complete la pregunta: ' + hiddenLabel);
              // Detener el proceso
              Swal.fire(
                'Revisa lo siguiente:',
                hiddenLabel
              )
              return false;
          }
          
          respuesta = {
            "id": idLabel,
            "pregunta": hiddenLabel,
            "respuesta": input.value,
            "valor": "" 
          };
          respuestas.push(respuesta);
          console.log(respuestas); 
      }

      const txt_comercio =  getCheckValues('txt_comercio');
      const txt_industria =  getCheckValues('txt_industria');
      const txt_sevicios =  getCheckValues('txt_sevicios');
      const txt_agropecuario =  getCheckValues('txt_agropecuario');
      console.log(txt_comercio.length)
      console.log(txt_industria.length)
      console.log(txt_sevicios.length)
      console.log(txt_agropecuario.length)
  
  
        if (txt_comercio.length == 0 && txt_comercio.length == 0 && txt_sevicios.length == 0 && txt_agropecuario.length == 0){
  
          Swal.fire(
            'Revisa lo siguiente:',
            'Por favor seleccione un sector',
          )
          return false
        }
      var xpreguntas = document.querySelectorAll('.diagnostico_pregunta');
      for (var i = 0; i < xpreguntas.length; i++) {
          var radios = xpreguntas[i].querySelectorAll('input[type="radio"]');
          var respondida = false;
          var radioName = '';
          var respuestaSeleccionada = '';
          for (var j = 0; j < radios.length; j++) {
              textoPregunta = xpreguntas[i].querySelector('.mdc-typography--body1').innerText;
              if (radios[j].checked) {
                  respondida = true;
                  respuestaSeleccionada = radios[j].value;
                  radioName = radios[j].getAttribute('name'); // Aquí obtenemos el nombre (name) del radio
                  respuesta = {
                    "id": radioName,
                    "pregunta": textoPregunta,
                    "respuesta": respuestaSeleccionada,
                    "valor": "" 
                  };
                  respuestas.push(respuesta);
                 
              }
              
            
          }
          if (!respondida) {
              var textoPregunta = xpreguntas[i].querySelector('.mdc-typography--body1').innerText;
              alert('Por favor responda a la pregunta: ' + textoPregunta);
              return false;
          }
        
      }
      console.log(respuestas); 
      console.log(respuestas); 
      let txt_company_id = document.getElementById('txt_company_id').value

      let postData = {
        'txt_company_id':txt_company_id,
        'respuestas': respuestas
      }
  console.log(postData)
  let apiUrl = '/api/diagnostico/';

  swcms.postFetch(apiUrl, postData).then((data) => {
    Swal.fire(
      'Gracias por inscribirte en INNOVA MUJER HONDURAS',
      'En breve estarás recibiendo un correo electrónico ',
      'success'
    )
    window.location.href = "/diagnosticos/view/"+data.id;
    //window.setTimeout(() => { window.location.assign('/registros/im'); 
 // }, 3000);

  }).catch((error) => {
    console.log(error)
    Swal.fire(
      'Error de conexión',
      'Por favor revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
      'error'
    )
    document.getElementById('submitSaveButton').disabled = false;
  });
showMSJ('Éxito','Soliciud enviada con exito','success')
  
  return true;
  return false

    // Validación del campo de texto txt_company_name
    const property = 'txt_company_name'; 
    if (mdcAssignedVars[property].value === '') {   
        showMSJ('Por favor responda la pregunta:', '1 Nombre Completo', 'info');
        return false;
    } else {
        preguntas.push({
            "id": "txt_company_name",
            "pregunta": "1 Nombre Completo",
            "respuesta": mdcAssignedVars[property].value,
            "valor": 0
        });
    }

    // Continuar con más validaciones o acciones si es necesar

    const txt_2_6 =  getCheckValues('txt_2_6');

    if (txt_2_6.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','5. Si su respuesta es sí a la pregunta anterior ¿Usted tiene facilidad para utilizar aplicaciones y programas en dispositivos tecnológicos?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_7", "pregunta":"5. Si su respuesta es sí a la pregunta anterior ¿Usted tiene facilidad para utilizar aplicaciones y programas en dispositivos tecnológicos?","respuesta":txt_2_6[0],"valor":txt_2_6})
    }

    console.log(preguntas)
    console.log('¡2El botón fue clickead2o!');
});


function getCheckValues(name){ 
    var chkds = document.getElementsByName(name);
    var ele=[];
    for (var i = 0; i < chkds.length; i++)
    {
      if (chkds[i].checked)
      {
        ele.push(chkds[i].value);
      }
    } 
    return ele;
          
  }

  function getCheckPoints(name){ 
    var chkds = document.getElementsByName(name);
    var ele=0
    for (var i = 0; i < chkds.length; i++)
    {
      if (chkds[i].checked)
      {
        ele = ele + parseInt(chkds[i].attributes.valor.nodeValue) 
        
      }
    } 
    return ele;
          
  }
function showMSJ(titulo,subtitulo,tipo){
    const Swal = swcms.returnSwal()
    Swal.fire(
      titulo,
      subtitulo,
      tipo
    )
  }
