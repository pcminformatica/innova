
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



function test_madurez_save(){

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



     
    property = 'txt_name_empresaria' 
    if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:','1 Nombre Completo','info')
        return false
    }else{
        preguntas.push({"id":"txt_name_empresaria","pregunta":"1 Nombre Completo","respuesta":mdcAssignedVars[property].value,"valor":0})
    }

    //1.2 N. Identidad:
    property = 'txt_name_empresa'
    if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:','2. Nombre de la empresa','info')
        return false
    }else{
        preguntas.push({"id":"txt_name_empresa","pregunta":"2 Nombre de la empresa","respuesta":mdcAssignedVars[property].value,"valor":0})
    }
    
    const cuenta_con_equipo =  getCheckValues('cuenta_con_equipo');
    const cuenta_con_equipo_total = getCheckPoints('cuenta_con_equipo')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','1. ¿Usted cuenta con equipo tecnológico?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_3", "pregunta":"1. ¿Usted cuenta con equipo tecnológico?","respuesta":cuenta_con_equipo[0],"valor":cuenta_con_equipo_total})
    }
   
    const equipo_tecnologico =  getCheckValues('equipo_tecnologico');
    const equipo_tecnologico_total = getCheckPoints('equipo_tecnologico')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','2. ¿Qué equipo tecnológico usa?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_4", "pregunta":"2. ¿Qué equipo tecnológico usa?","respuesta":equipo_tecnologico,"valor":equipo_tecnologico_total})
    }

    const interes_equipo_tecnologico =  getCheckValues('interes_equipo_tecnologico');
    const interes_equipo_tecnologico_total = getCheckPoints('interes_equipo_tecnologico')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3. ¿Qué interés tiene por el uso de equipo tecnológico?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_5", "pregunta":"3. ¿Qué interés tiene por el uso de equipo tecnológico?","respuesta":interes_equipo_tecnologico,"valor":interes_equipo_tecnologico_total})
    }
    
    const conoce_programas =  getCheckValues('conoce_programas');
    const conoce_programas_total = getCheckPoints('conoce_programas')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','4. Conoce o identifica programas o aplicación que se utilizan en dispositivos tecnológicos, por ejemplo: redes sociales, paquetes de office, herramientas para reuniones virtuales unica','info')
      return false
    }else{
      preguntas.push({"id":"TMD_6", "pregunta":"4. Conoce o identifica programas o aplicación que se utilizan en dispositivos tecnológicos, por ejemplo: redes sociales, paquetes de office, herramientas para reuniones virtuales unica","respuesta":conoce_programas[0],"valor":conoce_programas_total})
    }

    const tiene_facilidad =  getCheckValues('tiene_facilidad');
    const tiene_facilidad_total = getCheckPoints('tiene_facilidad')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','5. Si su respuesta es sí a la pregunta anterior ¿Usted tiene facilidad para utilizar aplicaciones y programas en dispositivos tecnológicos?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_7", "pregunta":"5. Si su respuesta es sí a la pregunta anterior ¿Usted tiene facilidad para utilizar aplicaciones y programas en dispositivos tecnológicos?","respuesta":tiene_facilidad[0],"valor":tiene_facilidad_total})
    }

    const habilidades_tecnologicas =  getCheckValues('habilidades_tecnologicas');
    const habilidades_tecnologicas_total = getCheckPoints('habilidades_tecnologicas')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','6. ¿Considera que tiene habilidades utilizando herramientas tecnológicas tales como?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_8", "pregunta":"6. ¿Considera que tiene habilidades utilizando herramientas tecnológicas tales como?","respuesta":habilidades_tecnologicas,"valor":habilidades_tecnologicas_total})
    }

    const herramientas_colaboracion =  getCheckValues('herramientas_colaboracion');
    const herramientas_colaboracion_total = getCheckPoints('herramientas_colaboracion')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','7. ¿Puede utilizar herramientas de colaboración en línea, como archivos y trabajar en proyectos de manera conjunta?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_9", "pregunta":"7. ¿Puede utilizar herramientas de colaboración en línea, como archivos y trabajar en proyectos de manera conjunta?","respuesta":herramientas_colaboracion[0],"valor":herramientas_colaboracion_total})
    }

    const conocimientos_seguridad =  getCheckValues('conocimientos_seguridad');
    const conocimientos_seguridad_total = getCheckPoints('conocimientos_seguridad')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','8. ¿Tiene conocimientos básicos de seguridad cibernética y protección de datos?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_10", "pregunta":"8. ¿Tiene conocimientos básicos de seguridad cibernética y protección de datos?","respuesta":conocimientos_seguridad[0],"valor":conocimientos_seguridad_total})
    }
    

    const habilidades_digitales =  getCheckValues('habilidades_digitales');
    const habilidades_digitales_total = getCheckPoints('habilidades_digitales')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','9. ¿Cómo calificaría su nivel de habilidades digitales?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_11", "pregunta":"9. ¿Cómo calificaría su nivel de habilidades digitales?","respuesta":habilidades_digitales[0],"valor":habilidades_digitales_total})
    }
    
    const experiencia_adoptar_herramientas =  getCheckValues('experiencia_adoptar_herramientas');
    const experiencia_adoptar_herramientas_total = getCheckPoints('experiencia_adoptar_herramientas')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','10. ¿Cómo considera que ha sido su experiencia al adoptar herramientas o tecnologías digitales en su vida personal o profesional?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_12", "pregunta":"10. ¿Cómo considera que ha sido su experiencia al adoptar herramientas o tecnologías digitales en su vida personal o profesional?","respuesta":experiencia_adoptar_herramientas[0],"valor":experiencia_adoptar_herramientas_total})
    }
    
    const cambios_digitales =  getCheckValues('cambios_digitales');
    const cambios_digitales_total = getCheckPoints('cambios_digitales')
    if (cuenta_con_equipo.length == 0 ){   
      showMSJ('Por favor responda la pregunta:',' 11. ¿Cómo se considera en cuanto a los cambios tecnológicos y digitales?','info')
      return false
    }else{
      preguntas.push({"id":"TMD_13", "pregunta":" 11. ¿Cómo se considera en cuanto a los cambios tecnológicos y digitales?","respuesta":cambios_digitales[0],"valor":cambios_digitales_total})
    }
    total = cuenta_con_equipo_total+equipo_tecnologico_total+interes_equipo_tecnologico_total+conoce_programas_total+tiene_facilidad_total+habilidades_tecnologicas_total+herramientas_colaboracion_total+conocimientos_seguridad_total+habilidades_digitales_total+experiencia_adoptar_herramientas_total+cambios_digitales_total
  


      let postData = {
        'txt_name': mdcAssignedVars['txt_name'].value.trim() || null,
        'txt_identidad': mdcAssignedVars['txt_identidad'].value.trim() || null,
        'txt_preguntas': preguntas,
        'total':total
        
      };

      console.log(preguntas)
      console.log(total)
      console.log(postData)
      let apiUrl = '/api/save/test/madurez/123/';
      document.getElementById('submitSaveButton').disabled = true;

      swcms.postFetch(apiUrl, postData).then((data) => {
        Swal.fire(
          'Gracias',
          'Bienvenida a INNOVA MUJER!',
          'success'
        )
        document.getElementById("step-1").style.display = "none"; 
        document.getElementById("step-2").style.display = 'block'; 
        
        document.getElementById("lbl_resultado").innerHTML = total;
      }).catch((error) => {
        Swal.fire(
          'Error de conexión',
          'Por favor intento de nuevo o revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
          'error'
        )
        document.getElementById('submitSaveButton').disabled = false;
        
      })
  }



  function encuestas_satifacion_save(){



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



    //1.1 Nombre Completo
    property = 'txt_name_empresaria'
    if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:','1.1 Nombre Completo','info')
        return false
    }else{
        preguntas.push({"id":"TMD_1","pregunta":"1.1 Nombre Completo","respuesta":mdcAssignedVars[property].value,"valor":0})
    }

    //1.2 N. Identidad:
    property = 'txt_name_empresa'
    if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:','2 Nombre de la empresa','info')
        return false
    }else{
        preguntas.push({"id":"TMD_2","pregunta":"2 Nombre de la empresa","respuesta":mdcAssignedVars[property].value,"valor":0})
    }
    
    const equipo_especialistas =  getCheckValues('equipo_especialistas');

    if (equipo_especialistas.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','3. ¿La atención del equipo de especialistas fue atenta y eficiente? ','info')
      return false
    }else{
      preguntas.push({"id":"equipo_especialistas", "pregunta":"3. ¿La atención del equipo de especialistas fue atenta y eficiente? ","respuesta":equipo_especialistas[0],"valor":0})
    }
   

    const tiempos_entrega =  getCheckValues('tiempos_entrega');

    if (tiempos_entrega.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','4. ¿Considera que los tiempos en la entrega de los productos o la asesoría son adecuados?','info')
      return false
    }else{
      preguntas.push({"id":"tiempos_entrega", "pregunta":"4. ¿Considera que los tiempos en la entrega de los productos o la asesoría son adecuados?","respuesta":tiempos_entrega[0],"valor":0})
    }

    const servicios_desarrollo =  getCheckValues('servicios_desarrollo');

    if (tiempos_entrega.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','5. ¿Los servicios de desarrollo empresarial brindados cumple con sus expectativas y necesidades?','info')
      return false
    }else{
      preguntas.push({"id":"servicios_desarrollo", "pregunta":"5. ¿Los servicios de desarrollo empresarial brindados cumple con sus expectativas y necesidades?","respuesta":servicios_desarrollo[0],"valor":0})
    }

    const considera_conocimientos =  getCheckValues('considera_conocimientos');

    if (tiempos_entrega.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','6. ¿Considera que los conocimientos técnicos aplicados por las personas especialistas son adecuados para el apoyo a su empresa?','info')
      return false
    }else{
      preguntas.push({"id":"considera_conocimientos", "pregunta":"6. ¿Considera que los conocimientos técnicos aplicados por las personas especialistas son adecuados para el apoyo a su empresa?","respuesta":considera_conocimientos[0],"valor":0})
    }

    const proceso_asesorias =  getCheckValues('proceso_asesorias');

    if (tiempos_entrega.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','7. ¿En el proceso de sus asesorías se utilizó un lenguaje claro y entendible?','info')
      return false
    }else{
      preguntas.push({"id":"proceso_asesorias", "pregunta":"7. ¿En el proceso de sus asesorías se utilizó un lenguaje claro y entendible?","respuesta":proceso_asesorias[0],"valor":0})
    }

    const especialistas_mostrado =  getCheckValues('especialistas_mostrado');

    if (tiempos_entrega.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','8. ¿Las personas especialistas han mostrado empatía ante su situación personal y de la empresa?','info')
      return false
    }else{
      preguntas.push({"id":"especialistas_mostrado", "pregunta":"8. ¿Las personas especialistas han mostrado empatía ante su situación personal y de la empresa?","respuesta":especialistas_mostrado[0],"valor":0})
    }

    const experiencia_vivida =  getCheckValues('experiencia_vivida');

    if (tiempos_entrega.length == 0 ){   
      showMSJ('Por favor responda la pregunta:','9. Como considera la experiencia vivida en el uso de la plataforma INNOVA ','info')
      return false
    }else{
      preguntas.push({"id":"experiencia_vivida", "pregunta":"9.Como considera la experiencia vivida en el uso de la plataforma INNOVA ","respuesta":experiencia_vivida[0],"valor":0})
    }



    property = 'txt_company_description'
    if (mdcAssignedVars[property].value === '' ){   
        showMSJ('Por favor responda la pregunta:','Comentarios y sugerencias','info')
        return false
    }else{
        preguntas.push({"id":"txt_company_description","pregunta":"Comentarios y sugerencias","respuesta":mdcAssignedVars[property].value,"valor":0})
    }

      let postData = {
        'txt_preguntas': preguntas,
        'txt_company':document.getElementById('txt_company').value
        
      };

      console.log(preguntas)
      
      console.log(postData)
  
      let apiUrl = '/api/save/catalog/surveys';
      document.getElementById('submitSaveButton').disabled = true;

      swcms.postFetch(apiUrl, postData).then((data) => {
        Swal.fire(
          'Gracias',
          'Encuesta enviada a INNOVA MUJER!',
          'success'
        )
        
        window.location.href = '/home/'
      }).catch((error) => {
        Swal.fire(
          'Error de conexión',
          'Por favor intento de nuevo o revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
          'error'
        )
        document.getElementById('submitSaveButton').disabled = false;
        
      })
  }