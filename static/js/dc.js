


window.addEventListener('load', function() {
    const mdcAssignedVars = {};
    console.log(mdcAssignedVars)
    console.log('All assets are loaded')
    const Swal = swcms.returnSwal()
    swcms.mdcTabBars.forEach((sel) => {
        console.log('siii')
      if (sel.assignedVar)
          mdcAssignedVars[sel.assignedVar] = sel;
    });
    console.log(mdcAssignedVars)
    var contentEls = document.querySelectorAll('.content');

    mdcAssignedVars['profiles'].listen('MDCTabBar:activated', function(event) {
      // Hide currently-active content
      document.querySelector('.content--active').classList.remove('content--active');
      // Show content for newly-activated tab
      contentEls[event.detail.index].classList.add('content--active');
    });
})

function loadFile(event){
  const Swal = swcms.returnSwal()
  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function() {
    URL.revokeObjectURL(output.src) // free memory
  }



}