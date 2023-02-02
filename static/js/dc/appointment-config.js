var mdcAssignedVars = {};

window.addEventListener('load', function() {

    console.log('All assets are loaded')
    const Swal = swcms.returnSwal()
    mdcAssignedVars = {}
    swcms.mdcDataTables.forEach((sel) => {
        console.log('siii')
      if (sel.assignedVar)
          mdcAssignedVars[sel.assignedVar] = sel;
    });
    console.log(mdcAssignedVars)
    
})

var calendar = {};

function saveCalender(){
    console.log('sss')
    calendar = {};
    let cupos = 0
    
    for (const property in mdcAssignedVars) {
     
        horas = []
        mdcAssignedVars[property].rowCheckboxList.forEach(function(row) {
        
            if (row.foundation.currentCheckState==='checked'){
                if (calendar[property]=== undefined || calendar[property] === null){
                    //creamos una json con la propidad del dia
                    calendar[property] = {'horas':[row.root.firstElementChild.value],'cupos':0};
                    //luego almacenamos en un arreglo la hora
                  
                }else{
                   
                    calendar[property].horas.push(row.root.firstElementChild.value);
                }
            }
        });
        cupos = document.querySelector('#calendar-'+property).value
        if (calendar[property] != undefined || calendar[property] != null){
            //creamos una json con la propidad del dia
           
            //luego almacenamos en un arreglo la hora
            calendar[property].cupos = cupos;
         
        }

  



        
    }
    let config = {};
    config['calendar'] = calendar
    console.log(config)
    const Swal = swcms.returnSwal()
    Swal.fire({
        title: '¿Desea  almacenar su calendario?',
        text: 'Para guardar da clic en,Si, Acepto ',

        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, Acepto'
      }).then((result) => {
        if (result.isConfirmed) {
            let apiUrl = '/api/save/config/calendar';
            let postData = {'config_json':config}
            swcms.postFetch(apiUrl, postData).then((data) => {
              Swal.fire(
                'Gracias',
                'Bienvenida a INNOVA MUJER!',
                'success'
              )
             // window.setTimeout(() => { window.location.assign('/home/'); }, 3000);
            }).catch((error) => {
        
                Swal.fire(
                    'Error de conexión',
                    'Por favor intento de nuevo o revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
                    'error'
                  )
             // document.getElementById('submitSaveButton').disabled = false;
            });
          }
      })

    const date = new Date()
    initCalendar(date.toISOString().split('T')[0])
}

function initCalendar(dateValue){
//    console.log('siiiiiiiiiiiiiiiii',dateValue)

    const [year,month, day] = dateValue.split('-');
    //string to date
    const date = new Date(+year, +month - 1, +day, +0, +0, +0);
    console.log(date + 'siiiiiiiiii')
    console.log(date.getDay())
    console.log(day)
    console.log('day---')

    //definimos la fecha de inicio
    const startDate = new Date(date);
    // definimos el rango de dias del calendario (7 dias)
    let endDate = new Date(date); endDate.setDate( endDate.getDate() + 6 )
    //creamos el arreglo de semas

    document.querySelector('#content-tab').innerHTML = '';
    document.querySelector('#tab-Calendar').innerHTML = '';

    const dates = [];
    while (startDate <= endDate) {
      dates.push(new Date(startDate));
      startDate.setDate(startDate.getDate() + 1);
    }
    let first = true;
    let tabContainer;
    let content;
    dates.forEach(function(date) {

        if(typeof calendar[dayOfWeekAsString(date.getDay())] !== "undefined"){
            console.log(date)
            console.log('--undefined--')
            tabContainer = createTabsElementCalendar(dayOfWeekAsString(date.getDay()),first)
            document.querySelector('#tab-Calendar').appendChild(tabContainer);
            content = createElementContentCalendar(dayOfWeekAsString(date.getDay()),first)
            document.querySelector('#content-tab').appendChild(content);

            calendar[dayOfWeekAsString(date.getDay())].horas.forEach(function(hour) {
                
                console.log('hour')
                //let va = availableDates(dayOfWeekAsString(date.getDay()),hour)
                console.log('crear')

                let calendarContainer = createElementCalendar(date,hour)
                console.log('appointment-hours-'+dayOfWeekAsString(date.getDay()))
                document.querySelector('#appointment-hours-'+dayOfWeekAsString(date.getDay())).appendChild(calendarContainer);
            });

            first = false
        }



    })


}
function jsonDatesV2(){
    //recorre los dias del calendario
    for (const day in calendar) {
        console.log('days')
        console.log(day)
        calendar[day].forEach(function(hour) {
            console.log('hour')
            let va = availableDates(day,hour)
            console.log('crear')
            let calendarContainer = createElementCalendar(hour)
            document.querySelector('#appointment-hours-'+day).appendChild(calendarContainer);
        });
    }

    let date = stringDate('2022-12-05 09:00:00')
    console.log(date);
    console.log(dayOfWeekAsString(date.getDay()))
    }

function jsonDates(){
    let dates = ['2022-12-05 09:00:00','2022-12-05 11:00:00']
    return dates
}

function availableDates(day,hour){
    console.log('availableDates')
    let appointments = jsonDates()
    appointments.forEach(function(appointment) {
        let x = stringDate(appointment);
        console.log(x)
        console.log('day: ', x.getHours())
        return;
        console.log('hora: ', x.getHours())
        if (day){

        }
    });
}

function stringDate(str){

    const [dateValues, timeValues] = str.split(' ');
    console.log(dateValues); //  "09/24/2022"
    console.log(timeValues); // "07:30:14"
    
    const [year,month, day] = dateValues.split('-');
    const [hours, minutes, seconds] = timeValues.split(':');
    
    const date = new Date(+year, +month - 1, +day, +hours, +minutes, +seconds);
    return date;
}

function createElementCalendar(date,hours){
    let datetime = date.toISOString() .split("T")[0] + ' ' + hours;
    let cardContainer = document.createElement('div'); 
    let dataContainer = document.createElement('div');
    let title = document.createElement('div');
    let subtitle = document.createElement('div');  
    cardContainer.classList.add('mdc-card', 'mdc-card--color-on-primary');
    dataContainer.classList.add('mdc-card__primary-action')
    title.classList.add('mdc-typography--headline6','s-font-color-secondary');
    subtitle.classList.add('mdc-typography--subtitle2');

    title.textContent = hours;
    subtitle.textContent = datetime;

    cardContainer.setAttribute('onclick',"saveAppointment2('"+ datetime + "')")
    dataContainer.appendChild(title)
    dataContainer.appendChild(subtitle)
    cardContainer.appendChild(dataContainer)
    return cardContainer;
}

function createElementContentCalendar(data,first){
    let cardContainer = document.createElement('div'); 
    let dataContainer = document.createElement('div');

    cardContainer.classList.add('content');
    if (first){
        cardContainer.classList.add('content','content--active')
    }else{
        cardContainer.classList.add('content')
    }
    dataContainer.classList.add('container-appointment-hours')
    dataContainer.setAttribute('id','appointment-hours-'+data)
    cardContainer.setAttribute('id','content-'+data)
    cardContainer.appendChild(dataContainer)
    return cardContainer;
}


function createTabsElementCalendar(data,first){
    let btnContainer = document.createElement('button'); 
    let tabContainer = document.createElement('span');
    let tabtitle = document.createElement('span');

    let tabindicator = document.createElement('span');  
    let tabindicatorcontent = document.createElement('span'); 
    let tabripple = document.createElement('span'); 

    btnContainer.className = 'mdc-tab mdc-tab 123';

    btnContainer.setAttribute('role','tab')
    btnContainer.setAttribute('aria-selected','true')
    btnContainer.setAttribute('tabindex','0')
    btnContainer.setAttribute('onclick','changeTAB(this)')
    btnContainer.setAttribute('id',data)
    tabContainer.classList.add('mdc-tab__content')
    tabtitle.classList.add('mdc-tab__text-label')

    
    tabindicator.setAttribute('id','indicator-'+data)
    if (first){
        tabindicator.className =  'mdc-tab-indicator mdc-tab-indicator--active';
    }else{
        tabindicator.className =  'mdc-tab-indicator';
    }
    tabindicatorcontent.classList.add('mdc-tab-indicator__content','mdc-tab-indicator__content--underline');
    
    tabripple.classList.add('mdc-tab__ripple');

    tabtitle.textContent = data

    tabindicator.appendChild(tabindicatorcontent)
    tabContainer.appendChild(tabtitle)
    btnContainer.appendChild(tabContainer)
    btnContainer.appendChild(tabindicator)
    btnContainer.appendChild(tabripple)

    return btnContainer;
}

function dayOfWeekAsString(dayIndex) {
    return ["Domingo","Lunes", "Martes","Miercoles","Jueves","Viernes","Sabado"][dayIndex] || '';
}

function changeTAB(event){
    document.querySelector('.content--active').classList.remove('content--active');
    document.querySelector('.mdc-tab-indicator--active').classList.remove('mdc-tab-indicator--active');
    // Show content for newly-activated tab
    console.log('----',event.id)
    console.log(event)
    document.getElementById('indicator-'+event.id).classList.add('mdc-tab-indicator--active');
    document.getElementById('content-'+event.id).classList.add('content--active');

}
function saveAppointment(date){
    const Swal = swcms.returnSwal()

    let apiUrl = '/api/save/app';
    let postData = {'scheduled_dt':date}
    swcms.postFetch(apiUrl, postData).then((data) => {
      Swal.fire(
        'Gracias',
        'Bienvenida a INNOVA MUJER!',
        'success'
      )
     // window.setTimeout(() => { window.location.assign('/home/'); }, 3000);
    }).catch((error) => {

      Swal.fire(
        'Error de conexión',
        'Por favor intento de nuevo o revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
        'error'
      )
      document.getElementById('submitSaveButton').disabled = false;
    });
}