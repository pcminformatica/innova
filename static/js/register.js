const mdcAssignedVars = {};
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
function showMSJ(titulo,subtitulo,tipo){
  const Swal = swcms.returnSwal()
  Swal.fire(
    titulo,
    subtitulo,
    tipo
  )
}
 function saveRegisterForms(){
    

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
            
    });
    let preguntas = []
    //Pregunta A
    const txt_ofrece =  getCheckValues('txt_ofrece');
    if (txt_ofrece.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','¿Conoce los servicios que ofrece INNOVA?','info')
      return false
    }else{
      preguntas.push({"pregunta":"¿Conoce los servicios que ofrece INNOVA?","respuesta":txt_ofrece[0]})
    }
   
    //Pregunta B
    const servicios =  getCheckValues('servicios_requiere');
    if (servicios.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','¿Qué servicios requiere de INNOVA?','info')
      return false
    }else{
      preguntas.push({"pregunta":"¿Qué servicios requiere de INNOVA?","respuesta":servicios})
    }
    
    //Pregunta C
    let property = 'txt_servicios_considera'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    showMSJ('Éxito','Plan de Acción creado!','success')
    //Pregunta 1.1
    property = 'txt_name'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
  
    //Pregunta 1.2
    property = 'txt_identidad'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.3
    property = 'txt_telefono'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 1.4
    property = 'txt_depto'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 1.5
    property = 'txt_municipio'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    
    //Pregunta 1.6
    property = 'txt_emp_edad'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.7
    property = 'txt_contactar'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.8
    property = 'txt_correo'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.9
    property = 'txt_facebook'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    
    //Pregunta 1.10
    property = 'txt_red_social'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    // pregunta 1.11
    property = 'txt_medio_prefiere'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    // pregunta 2.1
    property = 'txt_educativo_aprobado'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    // pregunta 2.2
    const dispositivos =  getCheckValues('txt_dispositivos');
    if (dispositivos.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.2 Qué dispositivos utiliza para conexión a internet','info')
      return false
    }else{
      preguntas.push({"pregunta":"2.2 Qué dispositivos utiliza para conexión a internet","respuesta":dispositivos})
    }
    // pregunta 2.3
    const calidad_internet =  getCheckValues('txt_calidad_internet');
    if (calidad_internet.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.3 Calidad del Internet','info')
      return false
    }else{
      preguntas.push({"pregunta":"2.3 Calidad del Internet","respuesta":calidad_internet[0]})
    }  
    // pregunta 2.4
    const grupo_pertenece =  getCheckValues('txt_grupo_pertenece');
    if (grupo_pertenece.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.4 Pertenece a un grupo poblacional étnico','info')
      return false
    }else{
      preguntas.push({"pregunta":"2.4 Pertenece a un grupo poblacional étnico","respuesta":grupo_pertenece[0]})
    }  
    // pregunta 2.5 
    property = 'txt_origen_etnico'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    // pregunta 2.6
    const emp_cargo =  getCheckValues('txt_emp_cargo');
    if (emp_cargo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.6 Cargo que Ud. desempeña (puede seleccionar más de una opción)','info')
      return false
    }else{
      preguntas.push({"pregunta":"2.6 Cargo que Ud. desempeña (puede seleccionar más de una opción)","respuesta":emp_cargo})
    }  
    

showMSJ('Éxito','Plan de Acción creado!','success')
  
    console.log(preguntas)
    /*
    for (const property in mdcAssignedVars) {
        if(mdcAssignedVars[property].value === '' && mdcAssignedVars[property].required===true){
          console.log(`${property}: ${mdcAssignedVars[property]}`);
          
          
          Swal.fire(
            'Por favor complete la pregunta:',
            `${mdcAssignedVars[property].label.root.attributes.hiddenlabel.value}`,
            'info'
            
          )
    
          return false
        }
      }*/
}