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
    //Pregunta 3.22
    property = 'volumen_ventas_ultimo'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.23
    property = 'volumen_utilidades_ultimo'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.24
    const tuvo_acceso_credito =  getCheckValues('tuvo_acceso_credito');
    if (tuvo_acceso_credito.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','¿Conoce los servicios que ofrece INNOVA?','info')
      return false
    }else{
      preguntas.push({"pregunta":"¿Conoce los servicios que ofrece INNOVA?","respuesta":tuvo_acceso_credito[0]})
    }
    //Pregunta 3.25
    property = 'rango_activos'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.26
    property = 'monto_credito'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.27
    const tipo_financiera_obtenido =  getCheckValues('tipo_financiera_obtenido');
    if (tipo_financiera_obtenido.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','¿Conoce los servicios que ofrece INNOVA?','info')
      return false
    }else{
      preguntas.push({"pregunta":"¿Conoce los servicios que ofrece INNOVA?","respuesta":tipo_financiera_obtenido[0]})
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
    preguntas.push({"pregunta":"3.18 ¿Cuáles de los siguientes aspectos describe mejor su objetivo principal con la participación en INNOVAMUJER HONDURAS?","respuesta":tipo_financiera_obtenido[0]})

  showMSJ('Éxito','Plan de Acción creado!','success')

  console.log(preguntas)
}
 function saveRegisterFormsV2(){
    

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
      preguntas.push({"pregunta":"2.8 ¿Me podría por favor indicar cuáles de los siguientes cargos en su empresa son ocupados por un hombre o una mujer? ","respuesta":ocupaciones})
    }  
    //Pregunta 3.1
    property = 'txt_name_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.2
    const cuenta_local =  getCheckValues('cuenta_local');
    if (cuenta_local.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.2 ¿Cuenta con local propio o es alquilado?','info')
      return false
    }else{
      preguntas.push({"pregunta":"3.2 ¿Cuenta con local propio o es alquilado?","respuesta":cuenta_local[0]})
    }
    //Pregunta 3.3
    const empresa_formalizada =  getCheckValues('empresa_formalizada');
    if (empresa_formalizada.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.3 ¿Su empresa está formalizada?','info')
      return false
    }else{
      preguntas.push({"pregunta":"3.3 ¿Su empresa está formalizada?","respuesta":empresa_formalizada[0]})
    }
    //Pregunta 3.4
    property = 'txt_phone_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.5
    property = 'txt_depto_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.6
    property = 'txt_depto_municipio'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.7
    property = 'txt_city_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.8
    property = 'txt_company_address'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }
    //Pregunta 3.9
    property = 'txt_mail_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }    
    //Pregunta 3.10
    property = 'txt_social_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }   
    //Pregunta 3.11
    property = 'txt_fundation_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    }   
    //Pregunta 3.12
    property = 'txt_actividad_company'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    } 
    //Pregunta 3.13
    property = 'txt_company_porcentaje'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    } 
    //Pregunta 3.14
    const cuentan_junta_directiva =  getCheckValues('cuentan_junta_directiva');
    if (cuentan_junta_directiva.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.14 Su organización o cooperativa ¿Cuentan con una junta directiva?','info')
      return false
    }else{
      preguntas.push({"pregunta":"3.2 ¿Cuenta con local propio o es alquilado?","respuesta":cuentan_junta_directiva[0]})
    }
    //Pregunta 3.15
    property = 'txt_company_miembros_junta'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
    } 
    //Pregunta 3.16
    property = 'txt_company_miembros_mujeres'
    if (mdcAssignedVars[property].value === '' ){   
      showMSJ('Por favor responda la pregunta:',mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,'info')
      return false
    }else{
      preguntas.push({"pregunta":mdcAssignedVars[property].label.root.attributes.hiddenlabel.value,"respuesta":mdcAssignedVars[property].value})
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
    preguntas.push({"pregunta":"3.17 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?","respuesta":empleado_ultimo})

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
      showMSJ('Por favor responda la pregunta:',"3.18 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?",'info')
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
    preguntas.push({"pregunta":"3.18 ¿Cuántos empleados a tiempo completo tuvo su empresa en el último año?","respuesta":temp_empleado_ultimo})
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
    preguntas.push({"pregunta":"3.19 ¿Cuántos empleados a tiempo completo tuvo su empresa el año antepasado?","respuesta":tiempo_completo_2_year})
  
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
    preguntas.push({"pregunta":"3.20 ¿Cuántos empleados temporales tuvo su empresa en el año antepasado?","respuesta":temporales_2_year})
    
    //3.21
    const mercado_producto =  getCheckValues('mercado_producto');
    if (mercado_producto.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3.21 El mercado de su producto o servicio es (marque todas las opciones que apliquen)','info')
      return false
    }else{
      preguntas.push({"pregunta":"3.21 El mercado de su producto o servicio es (marque todas las opciones que apliquen)","respuesta":mercado_producto})
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