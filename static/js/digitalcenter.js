/************************** DIGITAL CENTER **************************/


/************************** FUNCTIONS **************************/
export function showDetailsCard(elShow, isFrontOrBack) {
    let elmBack = 'serv-b--' + elShow;
    let elmFront = 'serv-f--' + elShow;

    if (isFrontOrBack == 'b') {
        document.getElementById(elmFront).classList.remove('animate__animated', 'animate__flipInY');
        document.getElementById(elmFront).classList.add('container--hidden');
        document.getElementById(elmBack).classList.add('animate__animated', 'animate__flipInY');
        document.getElementById(elmBack).classList.remove('container--hidden');
    } else if (isFrontOrBack == 'f') {
        document.getElementById(elmBack).classList.remove('animate__animated', 'animate__flipInY');
        document.getElementById(elmBack).classList.add('container--hidden');
        document.getElementById(elmFront).classList.add('animate__animated', 'animate__flipInY');
        document.getElementById(elmFront).classList.remove('container--hidden');
    }
}
/* Allow 'window' context to reference the function */
window.showDetailsCard = showDetailsCard;