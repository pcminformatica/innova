function acceptAppointments(){
    console.log('v2')
    const Swal = swcms.returnSwal()
    Swal.fire({
        title: '¿Deseas enviar un mensaje?',
        input: 'textarea',
        confirmButtonText: 'Enviar',
      }).then(function(result) {
        if (result.value) {
          //Swal.fire(result.value)
        }

        Swal.fire({
 
            icon: 'success',
            title: 'Mensaje enviado',
            showConfirmButton: false,
            timer: 1500
          })
      })
}

function acceptAppointments2(){
    console.log('v2')
    const Swal = swcms.returnSwal()
    Swal.fire({
        title: '¿Deseas enviar un mensaje?',
        input: 'date',
        confirmButtonText: 'Enviar',
      }).then(function(result) {
        if (result.value) {
          //Swal.fire(result.value)
        }

        Swal.fire({
 
            icon: 'success',
            title: 'Mensaje enviado',
            showConfirmButton: false,
            timer: 1500
          })
      })
}