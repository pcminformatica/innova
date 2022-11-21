


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



    let postData = {
      'uid': '1',
      'sid': '2',
      'eid': '3',
      'sch': '4',
      'udata': '5'
    };
    
    let apiUrl = '/api/accept/terminos/';
    //document.getElementById('submitSaveButton').disabled = true;
    swcms.postFetch(apiUrl, postData).then((data) => {
      Swal.fire('Siii')
  
    }).catch((error) => {
      Swal.fire('Nooo')
    //    document.getElementById('submitSaveButton').disabled = false;
    });
}

