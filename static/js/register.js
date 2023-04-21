const mdcAssignedVars = {};
const appCountry = 'HN';
window.addEventListener('load', function() {

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
  
  getStates()
})



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
    
    let preguntas = []

    //Pregunta A
    const txt_ofrece =  getCheckValues('txt_ofrece');
    if (txt_ofrece.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','¿Conoce los servicios que ofrece INNOVA?','info')
      return false
    }else{
      preguntas.push({"id":"A", "pregunta":"¿Conoce los servicios que ofrece INNOVA?","respuesta":txt_ofrece[0]})
    }
   
    //Pregunta B
    const servicios =  getCheckValues('servicios_requiere');
    if (servicios.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','¿Qué servicios requiere de INNOVA?','info')
      return false
    }else{
      preguntas.push({"id":"B","pregunta":"¿Qué servicios requiere de INNOVA?","respuesta":servicios})
    }
    
    //Pregunta C
    let property = 'txt_servicios_considera'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"C","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    showMSJ('Éxito','Plan de Acción creado!','success')
    //Pregunta 1.1
    property = 'txt_name'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_1","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
  
    //Pregunta 1.2
    property = 'txt_identidad'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_2","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.3
    property = 'txt_telefono'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_3","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 1.4
    property = 'txt_depto'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_4","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].selectedText.textContent})
    }
    //Pregunta 1.5
    property = 'txt_municipio'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_5","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].selectedText.textContent})
    }
    
    //Pregunta 1.6
    property = 'txt_emp_edad'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_6","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.7
    property = 'txt_contactar'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_7","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.8
    property = 'txt_correo'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }
    else if (valida_correo(mdcAssignedVars[property].value) == false){
      showMSJ('Tipo de correo no válido:','Pregunta 1.8 Correo','info')
      return false
    }
    else
    {  
      preguntas.push({"id":"1_8","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 1.9
    property = 'txt_facebook'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_9","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    
    //Pregunta 1.10
    property = 'txt_red_social'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_10","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    // pregunta 1.11
    property = 'txt_medio_prefiere'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"1_11","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    // pregunta 2.1
    property = 'txt_educativo_aprobado'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"2_1","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    // pregunta 2.2
    const dispositivos =  getCheckValues('txt_dispositivos');
    if (dispositivos.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.2 Qué dispositivos utiliza para conexión a internet','info')
      return false
    }else{
      preguntas.push({"id":"2_2","pregunta":"2.2 Qué dispositivos utiliza para conexión a internet","respuesta":dispositivos})
    }
    // pregunta 2.3
    const calidad_internet =  getCheckValues('txt_calidad_internet');
    if (calidad_internet.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.3 Calidad del Internet','info')
      return false
    }else{
      preguntas.push({"id":"2_3","pregunta":"2.3 Calidad del Internet","respuesta":calidad_internet[0]})
    }  
    // pregunta 2.4
    const grupo_pertenece =  getCheckValues('txt_grupo_pertenece');
    if (grupo_pertenece.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.4 Pertenece a un grupo poblacional étnico','info')
      return false
    }else{
      preguntas.push({"id":"2_4","pregunta":"2.4 Pertenece a un grupo poblacional étnico","respuesta":grupo_pertenece[0]})
    }  
    if (grupo_pertenece == 'SI'){
      // pregunta 2.5 
      property = 'txt_origen_etnico'
      if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
        return false
      }else{
        preguntas.push({"id":"2_5","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
      }
    }
    // pregunta 2.6
    const emp_cargo =  getCheckValues('txt_emp_cargo');
    if (emp_cargo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.6 Cargo que Ud. desempeña (puede seleccionar más de una opción)','info')
      return false
    }else{
      preguntas.push({"id":"2_6","pregunta":"2.6 Cargo que Ud. desempeña (puede seleccionar más de una opción)","respuesta":emp_cargo})
    }  
    // pregunta 2.7
    const participa_en_programas =  getCheckValues('participa_en_programas');
    if (participa_en_programas.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2.7 Actualmente usted participa de algún programa o proyecto de apoyo a la MIPYME: ','info')
      return false
    }else{
      preguntas.push({"id":"2_7", "pregunta":"2.7 Actualmente usted participa de algún programa o proyecto de apoyo a la MIPYME","respuesta":participa_en_programas[0]})
    }
    if (participa_en_programas == 'SI'){
      property = 'txt_especifique_programa'
      if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:','Especifique el o los programas o proyectos de apoyo a la MIPYME que usted participa','info')
        return false
      }else{
        preguntas.push({"id":"2_7_1","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
      }
      
    }
    // pregunta 2.8
    const accionista_principal =  getCheckValues('2_8_accionista_principal');
    const accionista_minoritaria =  getCheckValues('2_8_accionista_minoritaria');
    const propietaria_principal =  getCheckValues('2_8_propietaria_principal');
    const gerenta_general =  getCheckValues('2_8_gerenta_general');
    const gerenta_financiero =  getCheckValues('2_8_gerenta_financiero');
    const gerenta_operaciones =  getCheckValues('2_8_gerenta_operaciones');
    const presidenta_empresa =  getCheckValues('2_8_presidenta_empresa');
    const vicepresidenta =  getCheckValues('2_8_vicepresidenta');
    const representante_legal =  getCheckValues('2_8_representante_legal');
    const administradora =  getCheckValues('2_8_administradora');
  
    if (accionista_principal.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "A. Accionista principal" ')
      return false
    }else if  (accionista_minoritaria.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "B. Accionista Minoritaria" ')
      return false
    }else if  (propietaria_principal.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "C. Propietaria principal " ')
      return false
    }else if  (gerenta_general.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "D. Gerenta general" ')
      return false
    }else if  (gerenta_financiero.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "E. Gerenta financiero" ')
      return false
    }else if  (gerenta_operaciones.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "F. Gerenta de operaciones" ')
      return false
    }else if  (presidenta_empresa.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "G. Presidenta de la empresa" ')
      return false
    }else if  (vicepresidenta.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "H. Vicepresidenta" ')
      return false
    }else if  (representante_legal.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "I. Representante legal" ')
      return false
    }else if  (administradora.length == 0 ){   
      showMSJ('Por favor responda la pregunta: 2.8','Seleccione "J. Administradora" ')
      return false
    }else{
      const ocupaciones = {
        accionista_principal:accionista_principal[0],
        accionista_minoritaria:accionista_minoritaria[0],
        propietaria_principal:propietaria_principal[0],
        gerenta_general:gerenta_general[0],
        gerenta_financiero:gerenta_financiero[0],
        gerenta_operaciones:gerenta_operaciones[0],
        presidenta_empresa:presidenta_empresa[0],
        vicepresidenta:vicepresidenta[0],
        representante_legal:representante_legal[0],
        administradora:administradora[0],
      }
      preguntas.push({"id":"2_8","pregunta":"2.8 ¿Me podría por favor indicar cuáles de los siguientes cargos en su empresa son ocupados por un hombre o una mujer? ","respuesta":ocupaciones})
    }  
    //Pregunta 3.1
    property = 'txt_name_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_1","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.2
    const cuenta_local =  getCheckValues('cuenta_local');
    if (cuenta_local.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.2 ¿Cuenta con local propio o es alquilado?','info')
      return false
    }else{
      preguntas.push({"id":"3_2","pregunta":"3.2 ¿Cuenta con local propio o es alquilado?","respuesta":cuenta_local[0]})
    }
    //Pregunta 3.3
    const empresa_formalizada =  getCheckValues('empresa_formalizada');
    if (empresa_formalizada.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.3 ¿Su empresa está formalizada?','info')
      return false
    }else{
      preguntas.push({"id":"3_3","pregunta":"3.3 ¿Su empresa está formalizada?","respuesta":empresa_formalizada[0]})
    }
    //Pregunta 3.4
    property = 'txt_phone_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_4","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.5
    property = 'txt_depto_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_5","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].selectedText.textContent})
    }
    //Pregunta 3.6
    property = 'txt_depto_municipio'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_6","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].selectedText.textContent})
    }
    //Pregunta 3.7
    property = 'txt_city_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_7","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.8
    property = 'txt_company_address'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_8","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.9
    property = 'txt_mail_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }
    else if (valida_correo(mdcAssignedVars[property].value) == false){
      showMSJ('Tipo de correo no válido:','Pregunta 3.9 Correo','info')
      return false
    }
    else
    {  
      preguntas.push({"id":"3_9","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }

    //Pregunta 3.10
    property = 'txt_social_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_10","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }   
    //Pregunta 3.11
    property = 'txt_fundation_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_11","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }   
    //Pregunta 3.12
    property = 'txt_actividad_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_12","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    } 
    //Pregunta 3.13
    property = 'txt_company_porcentaje'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_13","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    } 
    //Pregunta 3.14
    const cuentan_junta_directiva =  getCheckValues('cuentan_junta_directiva');
    if (cuentan_junta_directiva.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.14 Su organización o cooperativa ¿Cuentan con una junta directiva?','info')
      return false
    }else{
      preguntas.push({"id":"3_14","pregunta":"3.14 Su organización o cooperativa ¿Cuentan con una junta directiva?","respuesta":cuentan_junta_directiva[0]})
    }
    //Pregunta 3.15
    property = 'txt_company_miembros_junta'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_15","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    } 
    //Pregunta 3.16
    property = 'txt_company_miembros_mujeres'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_16","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    } 
    //Pregunta 3.17
    property = 'txt_u_total_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?",'info')
      return false
    } 
    const u_total_mujer = mdcAssignedVars[property].value  

    property = 'txt_u_total_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?",'info')
      return false
    }
    const u_total_hombre = mdcAssignedVars[property].value

    property = 'txt_u_remunerados_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?",'info')
      return false
    }
    const u_remunerados_mujer = mdcAssignedVars[property].value
    

    property = 'txt_u_remunerados_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?",'info')
      return false
    }
    const u_remunerados_hombre = mdcAssignedVars[property].value
    
    
    property = 'txt_u_no_remunerados_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?",'info')
      return false
    }
    const u_no_remunerados_mujer = mdcAssignedVars[property].value
    

    property = 'txt_u_no_remunerados_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?",'info')
      return false
    }
    const u_no_remunerados_hombre = mdcAssignedVars[property].value
    
    
    const empleado_ultimo = {
      "u_total_mujer":u_total_mujer,
      "u_total_hombre":u_total_hombre,
      "u_remunerados_mujer":u_remunerados_mujer,
      "u_remunerados_hombre":u_remunerados_hombre,
      "u_no_remunerados_mujer":u_no_remunerados_mujer,
      "u_no_remunerados_hombre":u_no_remunerados_hombre
    }
    preguntas.push({"id":"3_17","pregunta":"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?","respuesta":empleado_ultimo})

    //Pregunta 3.18
    //Pregunta 3.17
    property = 'txt_temp_total_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.18 ¿Cuántos empleados temporales tuvo su empresa en el último año?",'info')
      return false
    } 
    const temp_total_mujer = mdcAssignedVars[property].value  

    property = 'txt_temp_total_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.18 ¿Cuántos empleados temporales tuvo su empresa en el último año?",'info')
      return false
    }
    const temp_total_hombre = mdcAssignedVars[property].value

    property = 'txt_temp_remunerados_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.18 ¿Cuántos empleados temporales tuvo su empresa en el último año?",'info')
      return false
    }
    const temp_remunerados_mujer = mdcAssignedVars[property].value
    

    property = 'txt_temp_remunerados_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.18 ¿Cuántos empleados temporales tuvo su empresa en el último año?",'info')
      return false
    }
    const temp_remunerados_hombre = mdcAssignedVars[property].value
    
    
    property = 'txt_temp_no_remunerados_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.18 ¿Cuántos empleados temporales tuvo su empresa en el último año?",'info')
      return false
    }
    const temp_no_remunerados_mujer = mdcAssignedVars[property].value
    

    property = 'txt_temp_no_remunerados_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.18 ¿Cuántos empleados temporales tuvo su empresa en el último año?",'info')
      return false
    }
    const temp_no_remunerados_hombre = mdcAssignedVars[property].value
    
    
    const temp_empleado_ultimo = {
      "temp_total_mujer":temp_total_mujer,
      "temp_total_hombre":temp_total_hombre,
      "temp_remunerados_mujer":temp_remunerados_mujer,
      "temp_remunerados_hombre":temp_remunerados_hombre,
      "temp_no_remunerados_mujer":temp_no_remunerados_mujer,
      "temp_no_remunerados_hombre":temp_no_remunerados_hombre
    }
    preguntas.push({"id":"3_18","pregunta":"3.18 ¿Cuántos empleados temporales tuvo su empresa en el último año?","respuesta":temp_empleado_ultimo})
    //3.19
    property = 'txt_compl_remunerados_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.19 ¿Cuántos empleados a tiempo completo tuvo su empresa el año antepasado?",'info')
      return false
    }
    const txt_compl_remunerados_mujer = mdcAssignedVars[property].value
    
  
    property = 'txt_compl_remunerados_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.19 ¿Cuántos empleados a tiempo completo tuvo su empresa el año antepasado?",'info')
      return false
    }
    const txt_compl_remunerados_hombre = mdcAssignedVars[property].value
    
    
    const tiempo_completo_2_year = {
      "txt_compl_remunerados_mujer":txt_compl_remunerados_mujer,
      "txt_compl_remunerados_hombre":txt_compl_remunerados_hombre
    }
    preguntas.push({"id":"3_19","pregunta":"3.19 ¿Cuántos empleados a tiempo completo tuvo su empresa el año antepasado?","respuesta":tiempo_completo_2_year})
  
    //3.20
    property = 'txt_temp_remunerados_2_mujer'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.20 ¿Cuántos empleados temporales tuvo su empresa en el año antepasado?",'info')
      return false
    }
    const temp_remunerados_2_mujer = mdcAssignedVars[property].value
    
  
    property = 'txt_temp_remunerados_2_hombre'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',"3.20 ¿Cuántos empleados temporales tuvo su empresa en el año antepasado?",'info')
      return false
    }
    const temp_remunerados_2_hombre = mdcAssignedVars[property].value
    const temporales_2_year = {
      "temp_remunerados_2_mujer":temp_remunerados_2_mujer,
      "temp_remunerados_2_hombre":temp_remunerados_2_hombre
    }
    preguntas.push({"id":"3_20","pregunta":"3.20 ¿Cuántos empleados temporales tuvo su empresa en el año antepasado?","respuesta":temporales_2_year})
    
    //3.21
    const mercado_producto =  getCheckValues('mercado_producto');
    if (mercado_producto.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.21 El mercado de su producto o servicio es (marque todas las opciones que apliquen)','info')
      return false
    }else{
      preguntas.push({"id":"3_21","pregunta":"3.21 El mercado de su producto o servicio es (marque todas las opciones que apliquen)","respuesta":mercado_producto})
    }
    //Pregunta 3.22
    property = 'volumen_ventas_ultimo'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_22","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.23
    property = 'volumen_utilidades_ultimo'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_23","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.24
    const tuvo_acceso_credito =  getCheckValues('tuvo_acceso_credito');
    if (tuvo_acceso_credito.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','En el último año, ¿su empresa tuvo acceso a crédito de alguna institución del sistema financiero (banco, cooperativa, micro financiera, caja de ahorros, etc.)?','info')
      return false
    }else{
      preguntas.push({"id":"3_24","pregunta":"En el último año, ¿su empresa tuvo acceso a crédito de alguna institución del sistema financiero (banco, cooperativa, micro financiera, caja de ahorros, etc.)?","respuesta":tuvo_acceso_credito[0]})
    }
    //Pregunta 3.25
    property = 'rango_activos'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_25","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    if (tuvo_acceso_credito=='SI'){
    //Pregunta 3.26
      property = 'monto_credito'
      if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
        return false
      }else{
        preguntas.push({"id":"3_26","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
      }
      //Pregunta 3.27
      const tipo_financiera_obtenido =  getCheckValues('tipo_financiera_obtenido');
      if (tipo_financiera_obtenido.length == 0 ){   
        showMSJ('Por favor responda la pregunta:','3.27 En qué tipo de institución financiera ha obtenido su crédito ','info')
        return false
      }else{
        preguntas.push({"id":"3_27","pregunta":"3.27 En qué tipo de institución financiera ha obtenido su crédito ","respuesta":tipo_financiera_obtenido[0]})
      }
    }
    //Pregunta 3.28
    property = 'services_mas_importantes'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }
    const services_mas_importantes = mdcAssignedVars[property].value
    property = 'services_importantes'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }
    const services_importantes = mdcAssignedVars[property].value
    property = 'services_menos_importantes'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }
    const services_menos_importantes = mdcAssignedVars[property].value
    const objetivos = {
      services_mas_importantes:services_mas_importantes,
      services_importantes:services_importantes,
      services_menos_importantes:services_menos_importantes,
    }
    preguntas.push({"id":"3_28","pregunta":"3.28 ¿Cuáles de los siguientes aspectos describe mejor su objetivo principal con la participación en INNOVAMUJER HONDURAS?","respuesta":objetivos})
    //Pregunta 3.29
    property = 'txt_cuanto_ascienden'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"3_25","pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //4.1
    const txt_estatus =  getCheckValues('txt_estatus');
    if (txt_estatus.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','4.1 Estatus','info')
      return false
    }else{
      preguntas.push({"id":"4_1","pregunta":"4.1 Estatus","respuesta":txt_estatus[0]})
    }
    //4.2
    const tipo_formalizacion =  getCheckValues('tipo_formalizacion');
    if (tipo_formalizacion.length == 0 ){   
      preguntas.push({"id":"4_2","pregunta":"4.2 Tipo de formalización","respuesta":""})
    }else{
      preguntas.push({"id":"4_2","pregunta":"4.2 Tipo de formalización","respuesta":tipo_formalizacion})
    }
    //4.3
    const tipo_organizacion =  getCheckValues('tipo_organizacion');

    preguntas.push({"id":"4_3","pregunta":"4.3 Registros pendientes ","respuesta":tipo_organizacion})
  
    //4.4
    property = 'como_se_entero'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"id":"4_4", "pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
        //Pregunta 4.5
        const confirmacion =  getCheckValues('checkbox_confirmacion');
        if (confirmacion.length == 0 ){   
          showMSJ('Por favor responda la pregunta:','4.5 Confirmación','info')
          return false
        }else{
          preguntas.push({"id":"4_5","pregunta":"4.5 Confirmación","respuesta":confirmacion})
        }
console.log(preguntas)
      const Swal = swcms.returnSwal()
  let postData = {
    'preguntas': preguntas
  }
  console.log(postData)
  let apiUrl = '/api/inscripciones/';
  document.getElementById('submitSaveButton').disabled = true;
  
  swcms.postFetch(apiUrl, postData).then((data) => {
    Swal.fire(
      'Gracias',
      'Bienvenida a INNOVA MUJER!',
      'success'
    )

    document.getElementById("corre_empresaria").innerHTML = mdcAssignedVars['txt_correo'].value
    document.getElementById("step-2").style.display = "block";
    document.getElementById("step-1").style.display = "none"; 
    //window.setTimeout(() => { window.location.assign('/registros/im'); 
 // }, 3000);

  }).catch((error) => {
    Swal.fire(
      'Error de conexión',
      'Por favor revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
      'error'
    )
    document.getElementById('submitSaveButton').disabled = false;
  });
showMSJ('Éxito','Soliciud enviada con exito','success')
  
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

function isNumberKey(evt){
  var charCode = (evt.which) ? evt.which : event.keyCode
  if (charCode > 31 && (charCode < 48 || charCode > 57))
      return false;
  return true;
}  

//Valida correo
function valida_correo(correo) {
  correo = correo.trim();
  console.log(correo)
  if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(correo)){
  
   return (true)
  } else {
   
   return (false);
  }
 }


 function getStates() {
  let cscApiKey = swcms.getApiDepKeys()

  let apiUrl = `https://api.countrystatecity.in/v1/countries/${appCountry}/states`;
  let headers = new Headers();
  let requestOptions = {
      method: 'GET',
      headers: headers,
      redirect: 'follow'
  };
  headers.append("X-CSCAPI-KEY", cscApiKey);
  swcms.getFetch(apiUrl, 'loadStates', requestOptions);
}

function loadStates(data) {

  let depListEl = document.querySelector('#f-appointment-department-select');
  let sortedData = data.sort((a, b) => a.name < b.name ? -1 : 1);

  sortedData.forEach((dep, index) => {
      let depContainer = document.createElement('li');
      let depRipple = document.createElement('span');
      let depName = document.createElement('span');

      depContainer.classList.add('mdc-deprecated-list-item');
      depRipple.classList.add('mdc-deprecated-list-item__ripple');
      depName.classList.add('mdc-deprecated-list-item__text');

      depName.textContent = dep.name.replace(' Department', '');
      depContainer.setAttribute('data-value', dep.iso2);

      depContainer.appendChild(depRipple);
      depContainer.appendChild(depName);
      depListEl.appendChild(depContainer);
   
      mdcAssignedVars['txt_depto'].menuItemValues[index] = dep.iso2;

      
  });
  // Call the following method whenever menu options are dynamically updated
  mdcAssignedVars['txt_depto'].layoutOptions();

  statesData = data;
  loadStates2(data)
}

function loadStates2(data) {


  let depListEl2 = document.querySelector('#f-appointment-department-select-2');
  let sortedData = data.sort((a, b) => a.name < b.name ? -1 : 1);

  sortedData.forEach((dep, index) => {
      let depContainer = document.createElement('li');
      let depRipple = document.createElement('span');
      let depName = document.createElement('span');

      depContainer.classList.add('mdc-deprecated-list-item');
      depRipple.classList.add('mdc-deprecated-list-item__ripple');
      depName.classList.add('mdc-deprecated-list-item__text');

      depName.textContent = dep.name.replace(' Department', '');
      depContainer.setAttribute('data-value', dep.iso2);

      depContainer.appendChild(depRipple);
      depContainer.appendChild(depName);
  
      depListEl2.appendChild(depContainer);

      mdcAssignedVars['txt_depto_company'].menuItemValues[index] = dep.iso2;
      
  });
  // Call the following method whenever menu options are dynamically updated


  mdcAssignedVars['txt_depto_company'].layoutOptions();
  statesData = data;

}
/* Allow 'window' context to reference the function */

function getCities(selState) {
  let cscApiKey = swcms.getApiDepKeys()
  if (selState) {
      let apiUrl = `https://api.countrystatecity.in/v1/countries/${appCountry}/states/${selState}/cities`;
      let headers = new Headers();
      let requestOptions = {
          method: 'GET',
          headers: headers,
          redirect: 'follow'
      };
      headers.append("X-CSCAPI-KEY", cscApiKey);
      swcms.getFetch(apiUrl, 'loadCities', requestOptions).then((data) => {

      });
  }
  
}
function getCities2(selState) {
  let cscApiKey = swcms.getApiDepKeys()
  if (selState) {
      let apiUrl = `https://api.countrystatecity.in/v1/countries/${appCountry}/states/${selState}/cities`;
      let headers = new Headers();
      let requestOptions = {
          method: 'GET',
          headers: headers,
          redirect: 'follow'
      };
      headers.append("X-CSCAPI-KEY", cscApiKey);
      swcms.getFetch(apiUrl, 'loadCities2', requestOptions).then((data) => {

      });
  }
  
}

function loadCities(data) {
  let citListEl = document.querySelector('#f-appointment-city-select');
  let sortedData = data.sort((a, b) => a.name < b.name ? -1 : 1);

  mdcAssignedVars['txt_municipio'].selectedIndex = -1;
  citListEl.innerHTML = '';

  sortedData.forEach((cit, index) => {
      let citContainer = document.createElement('li');
      let citRipple = document.createElement('span');
      let citName = document.createElement('span');

      citContainer.classList.add('mdc-deprecated-list-item');
      citRipple.classList.add('mdc-deprecated-list-item__ripple');
      citName.classList.add('mdc-deprecated-list-item__text');

      citName.textContent = cit.name;
      citContainer.setAttribute('data-value', cit.id);

      citContainer.appendChild(citRipple);
      citContainer.appendChild(citName);
      citListEl.appendChild(citContainer);

      mdcAssignedVars['txt_municipio'].menuItemValues[index] = cit.id;
  });
  
  // Call the following method whenever menu options are dynamically updated
  mdcAssignedVars['txt_municipio'].layoutOptions();
  
  citiesData = data;
}

function loadCities2(data) {
  let citListEl = document.querySelector('#f-appointment-city-select-2');
  let sortedData = data.sort((a, b) => a.name < b.name ? -1 : 1);

  mdcAssignedVars['txt_depto_municipio'].selectedIndex = -1;
  citListEl.innerHTML = '';

  sortedData.forEach((cit, index) => {
      let citContainer = document.createElement('li');
      let citRipple = document.createElement('span');
      let citName = document.createElement('span');

      citContainer.classList.add('mdc-deprecated-list-item');
      citRipple.classList.add('mdc-deprecated-list-item__ripple');
      citName.classList.add('mdc-deprecated-list-item__text');

      citName.textContent = cit.name;
      citContainer.setAttribute('data-value', cit.id);

      citContainer.appendChild(citRipple);
      citContainer.appendChild(citName);
      citListEl.appendChild(citContainer);

      mdcAssignedVars['txt_depto_municipio'].menuItemValues[index] = cit.id;
  });
  
  // Call the following method whenever menu options are dynamically updated
  mdcAssignedVars['txt_depto_municipio'].layoutOptions();
  
  citiesData = data;
}