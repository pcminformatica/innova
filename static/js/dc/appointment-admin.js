var appCal, currAppListElm, jsonSchedule, minDate, maxDate = null;
var currTab = 0;
const mdcAssignedVars = {};

const calendarx = {'Lunes': {'cupos': '2', 'horas': ['08:00', '09:00', '10:00']}, 'Martes': {'cupos': '2', 'horas': ['08:00', '09:00']}, 'Jueves': {'cupos': '2', 'horas': ['08:00', '09:00', '11:00']}, 'Viernes': {'cupos': '1', 'horas': ['08:00', '09:00']}, 'Sabado': {'cupos': '2', 'horas': ['08:00', '09:00', '11:00', '11:00', '12:00']}}
//const citas = {'citas':['2023-02-06 09:00:00','2023-02-06 10:00:00','2023-02-07 09:00:00']}

function showAppointments(date) {
    if (currAppListElm) {
        let hasApp = false;
        let nextDate = swcms.newDate(date);
        nextDate.setDate(nextDate.getDate() + 1);

        currAppListElm.querySelectorAll('.mdc-card').forEach((appointment) => {
            let appDate = swcms.newDate(parseInt(appointment.getAttribute('data-app-sess-s')));

            if (appDate.getTime() >= date.getTime() && appDate.getTime() < nextDate.getTime()) {
                appointment.classList.remove('container--hidden');
                hasApp = true;
            } else {
                appointment.classList.add('container--hidden');
            }
        });

        if (hasApp) {
            document.querySelector('.container-appointments-list--empty').classList.add('container--hidden');
            currAppListElm.classList.remove('container--hidden');
        } else {
            document.querySelector('.container-appointments-list--empty').classList.remove('container--hidden');
            currAppListElm.classList.add('container--hidden');
        }
    }
}

function createCalendarSchedule() {
    jsonSchedule = {};

    document.querySelectorAll('.container-appointments-list').forEach((container) => {
        let contId = container.getAttribute('id');
        let tabId = 0;

        switch (contId) {
            case 'container-appointments-list--createdby':
                tabId = 1;
                break;
        }

        container.querySelectorAll('.mdc-card').forEach((appointment) => {
            let contDate = swcms.returnFormatDate(parseInt(appointment.getAttribute('data-app-sess-s')), 'date');

            if (!(tabId in jsonSchedule)) {
                jsonSchedule[tabId] = [];
                jsonSchedule[tabId].push(contDate);
            } else {
                if (!(jsonSchedule[tabId].includes(contDate))) {
                    jsonSchedule[tabId].push(contDate);
                }
            }
        });
    });
}
function showAppointmentsTab(tabIndex) {
    currTab = tabIndex;
    if (currAppListElm) {
        currAppListElm.classList.add('container--hidden');
    }
    switch (tabIndex) {
        // My Appointments
        case 0:
            currAppListElm = document.getElementById('container-appointments-list--for');
            if (!currAppListElm) currAppListElm = document.getElementById('container-appointments-list--assigned');
            appCal.refresh();
            break;
        // Appointments Created By Me
        case 1:
            currAppListElm = document.getElementById('container-appointments-list--createdby');
            appCal.refresh();
            break;
    }
    return true;
}


window.addEventListener('load', () => {
    appCal = jsCalendar.get('#appointment-cal-admin');
    
    // Calendar configuration
    // Minimum date to allow is Today
    minDate = swcms.newDate();
    minDate.setDate(minDate.getDate() - 1);
    minDate.setHours(0);
    minDate.setMinutes(0);
    minDate.setSeconds(0);
    appCal.min(minDate);

    // Maximum date to allow is Two Months from now
    maxDate = swcms.newDate();
    maxDate.setMonth(maxDate.getMonth() + 2);
    maxDate.setHours(0);
    maxDate.setMinutes(0);
    maxDate.setSeconds(0);
    appCal.max(maxDate);
    
    // Click on date behavior
    appCal.onDateClick((event, date) => {
        appCal.set(date);
        console.log(date.toISOString().split('T')[0])
        initCalendar(date.toISOString().split('T')[0])
        
    });

    // Make changes on the date elements
	appCal.onDateRender((date, element, info) => {
        // Color weekends days red
        if (!info.isCurrent && (date.getDay() == 0 || date.getDay() == 6)) {
            element.classList.add((info.isCurrentMonth) ? 'jsCalendar-date-weekend-currentmonth' : 'jsCalendar-date-weekend-othermonth');
        }
        // Color days before and after MinDate and MaxDate grey
        if (date < minDate || date > maxDate) {
            element.classList.add('jsCalendar-date-unavailable');
            element.classList.remove('jsCalendar-date-weekend-currentmonth', 'jsCalendar-date-weekend-othermonth');
        }
        // Color days between Monday and Friday when Appointments are available
        if (jsonSchedule) {
            if (date.getDay() > 0 && date.getDay() < 6 && date > minDate && date < maxDate && info.isCurrentMonth) {
                if (info.isCurrent) {
                    element.classList.remove('jsCalendar-date-available');
                } else {
                    let formatDate = swcms.returnFormatDate(date, 'date');

                    if (currTab in jsonSchedule) {
                        if (jsonSchedule[currTab].includes(formatDate)) {
                            element.classList.add('jsCalendar-date-available');
                        }
                    }
                }
            }
        }

        // Show current date Appointments
        if (info.isCurrent) {
            showAppointments(date);
        }
    });

    // Create Calendar Analysis
    createCalendarSchedule();

	// Refresh Calendar layout - showAppointmentsTab has appCal.refresh()
    showAppointmentsTab(0);

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
});

var calendar

function initCalendar(dateValue){
    //    console.log('siiiiiiiiiiiiiiiii',dateValue)
    
        const [year,month, day] = dateValue.split('-');
        //string to date
        const date = new Date(+year, +month - 1, +day, +0, +0, +0);
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
        let dati = (document.querySelector('#app_svc_id').value)
        var regex = new RegExp("\'", "g");
        var res = dati.replace(regex, '"');
        calendar = JSON.parse(res)
 //       console.log(dati.replaceAll(/&quot;/ig,'"'));
 //       console.log(JSON.stringify(dati))
 //       calendar = JSON.parse("[{Lunes': {'cupos': '2', 'horas': ['08:00', '09:00', '10:00']}, 'Martes': {'cupos': '2', 'horas': ['08:00', '09:00', '10:00']}, 'Miercoles': {'cupos': '1', 'horas': ['08:00', '09:00', '10:00']}}]")
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

        disableDates()
        
    }

    function disableDates(){
        
        minDate = swcms.newDate();
        let dates = new Date();
        
        let datetime = dates.toISOString().split("T")[0] + ' 0:00:00';
        let emp_id = document.querySelector('#app_emp_id').value;
        console.log(datetime)
        console.log('datetime')

        let apiUrl = '/api/sde/calendar';
        let postData = {'date':datetime,'emp_id':emp_id}
        swcms.postFetch(apiUrl, postData).then((data) => {
            let countDay = []
            data.citas.forEach(function(date) {
                console.log('date:b')
                console.log(date)
                let x = date.replaceAll(' ','-').replaceAll(':','-').slice(0,-3)
                console.log('datetime')
                console.log(x)
                console.log('datetime')
                let elemento = document.querySelector('#div-'+x)
                if (elemento != undefined || elemento != null){
                    elemento.removeAttribute('onclick')
                    elemento.setAttribute('onclick',"reservada()")
                    elemento.className =  'mdc-card';
                    console.log(date)
                }
          
    
                //covertir el string en fecha
                dia = date.split(' ')[0]
                console.log(dia)
                date = stringDate(date)
                //tomamos los cupos que se pueden obtener al dìa          
                if (countDay[dia]=== undefined || countDay[dia] === null){
                    countDay[dia] = 1;
                }else{
                    countDay[dia] = countDay[dia] + 1;
                }
                //citas por dìas no supere los cupos
                if (countDay[dia] >= calendar[dayOfWeekAsString(date.getDay())].cupos){
                    console.log('ya no hay cupos')
    
                    let busqueda = document.querySelectorAll('.mdc-'+dia)
                    if (busqueda != undefined || busqueda != null){
                        busqueda.forEach((appointment) => {
                            appointment.removeAttribute('onclick')
                            appointment.setAttribute('onclick',"reservada()")
                            appointment.className =  'mdc-card';
                            console.log(date)
                        });
                   
                    }
                    
    
                }else{
                    console.log('si hay cupos')
     
                }
                
              
            })
          
         // window.setTimeout(() => { window.location.assign('/home/'); }, 3000);
        }).catch((error) => {
    
            console.log(
                'Error de conexión',
                'Por favor intento de nuevo o revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
                'error'
              )
         // document.getElementById('submitSaveButton').disabled = false;
        });

    }

    
    function stringDate(str){
    
        const [dateValues, timeValues] = str.split(' '); //  "09/24/2022", // "07:30:14"
        
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
    
        cardContainer.setAttribute('onclick',"selectAppointment('"+ datetime + "')")
        cardContainer.setAttribute('id','div-'+datetime.replaceAll(' ','-').replaceAll(':','-'))
        cardContainer.classList.add('mdc-'+date.toISOString() .split("T")[0]);
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


    function selectAppointment(date){

        const [dateValues, timeValues] = date.split(' '); //  "09/24/2022", // "07:30:14"
        document.querySelector('#container-appointment-confirm--date').innerHTML = dateValues;
        document.querySelector('#container-appointment-confirm--time').innerHTML = timeValues;
        document.querySelector('#app_sch_dt').value = date;
        
        return false
       
    }

    function saveAppointment(){
        
        const Swal = swcms.returnSwal()
        let date = document.querySelector('#app_sch_dt').value;
        let emp_id = document.querySelector('#app_emp_id').value;
        Swal.fire({
            title: '¿Desea  reservar cita?',
            text: date,

            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, Acepto',
            cancelButtonText:'Cancelar',
          }).then((result) => {
            if (result.isConfirmed) {
                let apiUrl = '/api/save/app';
                let postData = {'scheduled_dt':date,'emp_id':emp_id}
                swcms.postFetch(apiUrl, postData).then((data) => {
                  Swal.fire(
                    'Gracias',
                    'Cita almacenda con exito!',
                    'success'
                  )
                 // window.setTimeout(() => { window.location.assign('/home/'); }, 3000);
                 disableDates()
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



    }

    function reservada(){
        const Swal = swcms.returnSwal()
        Swal.fire(
            'Fecha ya reservada',
            'Por favor intento de nuevo o revisar tu conexión a internet, si el problema persiste contacta al administrador del sistema',
            'error'
          )
    }


    function Test(){
        const Swal = swcms.returnSwal()
        let apiUrl = '/api/sde/calendar';
        let postData = {'scheduled_dt':'date','emp_id':'emp_id'}
        swcms.postFetch(apiUrl, postData).then((data) => {
            let countDay = []
            data.citas.forEach(function(date) {
                console.log('date:b')
                console.log(date)
                let elemento = document.querySelector('#div-'+date.replaceAll(' ','-').replaceAll(':','-'))
                if (elemento != undefined || elemento != null){
                    elemento.removeAttribute('onclick')
                    elemento.setAttribute('onclick',"reservada()")
                    elemento.className =  'mdc-card';
                    console.log(date)
                }
          
    
                //covertir el string en fecha
                dia = date.split(' ')[0]
                console.log(dia)
                date = stringDate(date)
                //tomamos los cupos que se pueden obtener al dìa          
                if (countDay[dia]=== undefined || countDay[dia] === null){
                    countDay[dia] = 1;
                }else{
                    countDay[dia] = countDay[dia] + 1;
                }
                //citas por dìas no supere los cupos
                if (countDay[dia] >= calendar[dayOfWeekAsString(date.getDay())].cupos){
                    console.log('ya no hay cupos')
    
                    let busqueda = document.querySelectorAll('.mdc-'+dia)
                    if (busqueda != undefined || busqueda != null){
                        busqueda.forEach((appointment) => {
                            appointment.removeAttribute('onclick')
                            appointment.setAttribute('onclick',"reservada()")
                            appointment.className =  'mdc-card';
                            console.log(date)
                        });
                   
                    }
                    
    
                }else{
                    console.log('si hay cupos')
     
                }
                
              
            })
          Swal.fire(
            'Gracias',
            'Cita almacenda con exito!',
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



    function saveAppointmentAdmin(){
  
        const Swal = swcms.returnSwal()
        let date = document.querySelector('#app_sch_dt').value;
        let usr_id = document.querySelector('#app_usr_id').value;
        let emp_id = document.querySelector('#app_emp_id').value;
        let app_service_id = document.querySelector('#app_service_id').value;
        let postData = {'scheduled_dt':date,'emp_id':emp_id,'usr_id':usr_id,'app_service_id':app_service_id}
        console.log(postData)
        Swal.fire({
            title: '¿Desea  reservar cita?',
            text: date,

            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, Acepto',
            cancelButtonText:'Cancelar',
          }).then((result) => {
            if (result.isConfirmed) {
                let apiUrl = '/api/save/appointment/admin';
                
                swcms.postFetch(apiUrl, postData).then((data) => {
                  Swal.fire(
                    'Gracias',
                    'Cita almacenda con exito!',
                    'success'
                  )
                 // window.setTimeout(() => { window.location.assign('/home/'); }, 3000);
                 disableDates()
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



    }
