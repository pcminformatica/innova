
  const mdcAssignedVars = {};
window.addEventListener('load', function() {


  swcms.mdcDataTables.forEach((sel) => {
    if (sel.assignedVar)
        mdcAssignedVars[sel.assignedVar] = sel;
  });
  swcms.mdcSelects.forEach((sel) => {
    if (sel.assignedVar)
        mdcAssignedVars[sel.assignedVar] = sel;
  });
  swcms.mdcTextInputs.forEach((txt) => {
    if (txt.assignedVar)
        mdcAssignedVars[txt.assignedVar] = txt;
  });
  console.log(mdcAssignedVars)
  console.log('1111111')



})

function saveUsers(){
  
  const Swal = swcms.returnSwal()

  let postData = {
    'txt_name': mdcAssignedVars['txt_name'].value.trim() || null,
    'txt_email': mdcAssignedVars['txt_email'].value.trim() || null,
    'txt_rol': mdcAssignedVars['txt_rol'].value.trim() || null,
    'txt_id':document.getElementById('txt_id').value
  }
  console.log(postData)
  let apiUrl = '/api/save/user/admin';
  document.getElementById('submitSaveButton').disabled = true;

  swcms.postFetch(apiUrl, postData).then((data) => {
    Swal.fire(
      'Gracias',
      'Bienvenida a INNOVA MUJER!',
      'success'
    )
    window.setTimeout(() => { window.location.assign('/admin/list/user/'); 
  }, 3000);

  }).catch((error) => {
    Swal.fire(
      'Error de conexión',
      'Por favor revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
      'error'
    )
    document.getElementById('submitSaveButton').disabled = false;
  });
}

function saveService(){
  const Swal = swcms.returnSwal()
  let postData = {
    'txt_name': mdcAssignedVars['txt_name'].value.trim() || null,
    'txt_rol': mdcAssignedVars['txt_rol'].value.trim() || null,
    'txt_tiempo_asesoria': mdcAssignedVars['txt_tiempo_asesoria'].value.trim() || null,
    'txt_tiempo_ejecucion': mdcAssignedVars['txt_tiempo_ejecucion'].value.trim() || null,
    'txt_costo': mdcAssignedVars['txt_costo'].value.trim() || null,
    'txt_id':document.getElementById('txt_id').value
  }
  let apiUrl = '/api/save/user/service';
  document.getElementById('submitSaveButton').disabled = true;

  swcms.postFetch(apiUrl, postData).then((data) => {
    Swal.fire(
      'Gracias',
      'Modificado!',
      'success'
    )
    window.setTimeout(() => { window.location.reload(); 
  }, 1000);

  }).catch((error) => {
    Swal.fire(
      'Error de conexión',
      'Por favor revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
      'error'
    )
    document.getElementById('submitSaveButton').disabled = false;
  });
}

function saveUsersCompany(){
  const Swal = swcms.returnSwal()

  let postData = {
    'txt_company': mdcAssignedVars['txt_company'].value.trim() || null,
    'txt_id':document.getElementById('txt_id').value
  }

  let apiUrl = '/api/save/user/company/admin';
  console.log(postData)

  swcms.postFetch(apiUrl, postData).then((data) => {
    Swal.fire(
      'Gracias',
      'Modificado!',
      'success'
    )
    window.setTimeout(() => { window.location.reload(); 
  }, 1000);

  }).catch((error) => {
    Swal.fire(
      'Error de conexión',
      'Por favor revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
      'error'
    )
    document.getElementById('submitSaveButton').disabled = false;
  });

}