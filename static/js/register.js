const mdcAssignedVars = {};
function getCheckValues(name){
    console.log('servicios.2')
 
        var chkds = document.getElementsByName(name);
        var ele=[];
           for (var i = 0; i < chkds.length; i++)
            {
              if (chkds[i].checked)
              {
                ele.push(chkds[i].value);
              }
           }  console.log('servicios.3')
          return ele;
         
   
      
}

 function saveRegisterForms(){
    const Swal = swcms.returnSwal()

    
    swcms.mdcCheckbox.forEach((sel) => {
        if (sel.assignedVar)
            mdcAssignedVars[sel.assignedVar] = sel;
            
    });
    console.log('servicios.length')

    const servicios =  getCheckValues('servicios_requiere');

    if (servicios.length == 0 ){
        
        Swal.fire(
            'Por favor complete el pregunta:',
            `¿Qué servicios requiere de INNOVA?`,
            'info'
            
          )
        return false
    }
    console.log('servicios.4')
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
          
          
          Swal.fire(
            'Por favor complete la pregunta:',
            `${mdcAssignedVars[property].label.root.attributes.hiddenlabel.value}`,
            'info'
            
          )
    
          return false
        }
      }
}