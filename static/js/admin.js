const mdcAssignedVars = {};

function acceptterms(){
    console.log('v2')
    const Swal = swcms.returnSwal()
    var checkboxes = document.getElementsByName('cxb_accept');
    // loop over them all
    let accept = true;
    for (var i=0; i<checkboxes.length; i++) {
       // And stick the checked ones onto an array...
       if (!checkboxes[i].checked) {
        accept = false
       }
    }

    if (accept){
      let apiUrl = '/api/accept/terminos/';
      document.getElementById('submitSaveButton').disabled = false;
      let postData = {}
      swcms.postFetch(apiUrl, postData).then((data) => {
        Swal.fire(
          'Gracias',
          'Bienvenida a INNOVA MUJER!',
          'success'
        )
        window.setTimeout(() => { window.location.assign('/home/'); }, 3000);
      }).catch((error) => {

        Swal.fire(
          'Error de conexión',
          'Por favor revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
          'error'
        )
        document.getElementById('submitSaveButton').disabled = true;
      });
    }else{
      document.getElementById('submitSaveButton').disabled = true;
      Swal.fire(
        'Por favor acepté todos los términos',
        'Para ingresar al proyecto, necesita cumplir con los requisitos indicados en el formulario',
        'info'
      )
    }


}


function saveCompanyForms(){
  const Swal = swcms.returnSwal()
  swcms.mdcSelects.forEach((sel) => {
    if (sel.assignedVar)
        mdcAssignedVars[sel.assignedVar] = sel;
  });
  swcms.mdcTextInputs.forEach((txt) => {
    if (txt.assignedVar)
        mdcAssignedVars[txt.assignedVar] = txt;
  });
  for (const property in mdcAssignedVars) {
    if(mdcAssignedVars[property].value === '' && mdcAssignedVars[property].required===true){
      console.log(`${property}: ${mdcAssignedVars[property]}`);
      mdcAssignedVars[property].required
      Swal.fire(`Por favor complete el campo: ${mdcAssignedVars[property].label.root.innerText} `)
      Swal.fire(
        'Por favor complete el campo:',
        `${mdcAssignedVars[property].label.root.innerText}`,
        'info'
        
      )

      return false
    }
  }
  
    let postData = {
      'txt_name': mdcAssignedVars['txt_name'].value.trim() || null,
      'txt_last': mdcAssignedVars['txt_last'].value.trim() || null,
      'txt_dni': mdcAssignedVars['txt_dni'].value.trim() || null,
      'txt_company_name': mdcAssignedVars['txt_company_name'].value.trim() || null,
      'txt_company_rtn': mdcAssignedVars['txt_company_rtn'].value.trim() || null,
      'txt_company_phone':mdcAssignedVars['txt_company_phone'].value.trim() || null,
      'txt_company_facebook':mdcAssignedVars['txt_company_facebook'].value.trim() || null,
      'txt_company_instagram':mdcAssignedVars['txt_company_instagram'].value.trim() || null,
      'txt_company_address':mdcAssignedVars['txt_company_address'].value.trim() || null,
      'txt_company_description':mdcAssignedVars['txt_company_description'].value.trim() || null,
      'txt_company_public':document.getElementById("checkbox-public").checked
      
    };
    console.log(postData)

      let apiUrl = '/api/save/perfil/';
      document.getElementById('submitSaveButton').disabled = false;

      swcms.postFetch(apiUrl, postData).then((data) => {
        Swal.fire(
          'Gracias',
          'Bienvenida a INNOVA MUJER!',
          'success'
        )
        window.setTimeout(() => { window.location.assign('/home/'); }, 3000);
    
      }).catch((error) => {
        Swal.fire(
          'Error de conexión',
          'Por favor revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
          'error'
        )
        document.getElementById('submitSaveButton').disabled = true;
      });

}


function saveCategory(){
  const Swal = swcms.returnSwal()
  Swal.fire(
    'Gracias',
    'Bienvenida a INNOVA MUJER!',
    'success'
  )
  window.setTimeout(() => { window.location.assign('/home/'); }, 2000);
}




