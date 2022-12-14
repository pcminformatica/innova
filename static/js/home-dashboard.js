/************************** HOME DASHBOARD **************************/


/************************** FUNCTIONS **************************/
export function showMessagesContracts(index) {
    switch (index) {
        // Show Messages
        case 0:
            document.querySelector('.container-dashboard--messages-cnt').classList.add('container--hidden');
            document.querySelector('.container-dashboard--messages-msg').classList.remove('container--hidden');
            break;
        // Show Contracts
        case 1:
            document.querySelector('.container-dashboard--messages-msg').classList.add('container--hidden');
            document.querySelector('.container-dashboard--messages-cnt').classList.remove('container--hidden');
            break;
    }
}

export function showRedirect(url,target='self') {
    if(target=='self'){
        window.location.assign(url);
 
    }else{
        window.open(url);
    }
}

/* Allow 'window' context to reference the function */
window.showMessagesContracts = showMessagesContracts;
window.showRedirect = showRedirect;