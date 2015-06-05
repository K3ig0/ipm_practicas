(function () {
    function init() {
        var date = new Date();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        Calendar(month, year);
    }
    window.addEventListener('load', init, false);
})();

Calendar = function (month, year) {
    var events = [];
    var user = [];
    var subjects = [];
    var validData;
    bindAllListeners();
    changeMonth(year, month);
    
    function changeMonth(year, month) {
        prepareView(year, month);
        removeAllMarks(); // borramos las descripciones anteriores y esperamos por los datos
        clearDescription();
        showLoading();
        
        var xhr = new XMLHttpRequest();
        var token = Math.random();
        validData = token;
        xhr.onreadystatechange=function() {
            if (token != validData) // si la peticion ya ha expirado salimos
                return;
            if (xhr.readyState==4) {
                switch (xhr.status) {
                    case 200: // OK!
                        response = JSON.parse(xhr.responseText);
                        markDays(response);
                    break;
                    case 404: // Error: 404 - Resource not found!
                        alert("Resource not found!");
                    break;
                    default: // Error: Unknown!
                }
            }
       }
       xhr.open('GET', 'http://localhost:8080/cgi-bin/month.py?year=' + year + '&month=' + month, true);
       xhr.send();
    }
    
    function bindAllListeners() {
        document.querySelector("#atras").addEventListener('click', onPrevMonth, false);
        document.querySelector("#atras").addEventListener('keydown', function(e){if(e.keyCode === 13)onPrevMonth();}, false);
        document.querySelector("#adelante").addEventListener('click', onNextMonth, false);
        document.querySelector("#adelante").addEventListener('keydown', function(e){if(e.keyCode === 13)onNextMonth();}, false);
        var days = document.querySelectorAll(".day");
        for (i=0; i < days.length; i++) {
           days[i].addEventListener('click', onClickDay, false);
           days[i].addEventListener('keydown', function(e){if(e.keyCode === 13)onClickDay(e);}, false);
        }
        
        document.querySelector("#login").addEventListener('click', onShowLogin, false);
        document.querySelector("#dialog form").addEventListener('submit', onLogin, false);
        document.querySelector("#cancel").addEventListener('click', onCancelLogin, false);
        document.querySelector("#logout").addEventListener('click', onLogout, false);
        document.querySelector("#view_by_subject").addEventListener('change', onSubjectChange, false);
        document.querySelector("#busqueda").addEventListener('change', onSearch, false);
    }
    
    function removeAllMarks() {
        var placeHolder = document.querySelectorAll(".day-content");
        var day = document.querySelectorAll(".day");
        for (i=0; i < placeHolder.length; i++) {
            placeHolder[i].innerHTML = "";
            day[i].classList.remove("marked");
        }
    }
    
    function markDays(data) {
        //[[doc.subtype, doc.subjects]]
        events = data;
        for (i=0; i < data.length; i++) {
            if (user.length == 0 || subjects.indexOf(data[i][2][0]) != -1) {
                document.querySelector("#day" + data[i][0] + " .day-content").innerHTML += data[i][2][0] + " ";
                document.querySelector("#day" + data[i][0]).classList.add("marked");
            }
        }
        
        hideLoading();
    }
    
    function onNextMonth() {
        if (month == 12) {
            month = 1;
            year++;
        }
        else
            month++;
        changeMonth(year, month);
    }
    
    function onPrevMonth() {
        if (month == 1) {
            month = 12;
            year--;
        }
        else
            month--;
        changeMonth(year, month);
    }
    
    function onClickDay(e) {
        clearDescription();
        var day;
        console.log(e.target.className);
        if (e.target.classList.contains("day")) day = parseInt(e.target.firstElementChild.innerHTML);
        else day = parseInt(this.firstElementChild.innerHTML);
        for (i=0; i < events.length; i++) {
            if (parseInt(events[i][0]) == day && (subjects.length == 0 || subjects.indexOf(events[i][2][0]) != -1)) {
                var span = document.createElement("li");
                span.appendChild(document.createTextNode(events[i][1] + " - " + events[i][2]));
                document.querySelector("#event-description").appendChild(span);
            }
        }
    }
    
    function onShowLogin() {
        document.querySelector("#dialog").setAttribute("aria-hidden",false);
        document.querySelector("#dialog").classList.remove("hidden");
    }
    
    function onLogin(e) {
        e.preventDefault();
        showLoading();
        document.querySelector("#dialog").setAttribute("aria-hidden",true);
        document.querySelector("#dialog").classList.add("hidden");
        var xhr = new XMLHttpRequest();
        var name = document.querySelector("#usuario").value;
        xhr.open('GET', '/cgi-bin/user.py?user=' + name, true);
        xhr.onload = function (e) {
            if (this.status == 200) {
                var response = JSON.parse(this.response);
                hideLoading();
                if (response.length == 1) {
                    user = response;
                    subjects = user[0][1];
                    changeMonth(year, month);
                    document.querySelector("#login").setAttribute("aria-hidden",true);
                    document.querySelector("#login").classList.add("hidden");
                    document.querySelector("#logout").setAttribute("aria-hidden",false);
                    document.querySelector("#logout").classList.remove("hidden");
                    if (user[0][0] == "teacher") {
                        var select = document.querySelector("#view_by_subject");
                        var option;
                        while(select.hasChildNodes()) { // primero limpiamos las opciones anteriores
                            select.removeChild(select.lastChild);
                        }
                        option = document.createElement("option");
                        option.setAttribute("value", "todo");
                        option.innerHTML = "todo";
                        select.appendChild(option);
                        for (i=0; i < subjects.length; i++) {
                            option = document.createElement("option");
                            option.setAttribute("value", subjects[i]);
                            option.innerHTML = subjects[i];
                            select.appendChild(option);
                        }
                        select.setAttribute("aria-hidden",false);
                        select.classList.remove("hidden");
                    }
                } else {
                    alert("Error: El usuario no ha sido encontrado en la base de datos.");
                }
            }
        }
        xhr.send();
    }
    
    function onCancelLogin(e) {
        document.querySelector("#dialog").setAttribute("aria-hidden",true);
        document.querySelector("#dialog").classList.add("hidden");
        e.preventDefault();
    }
    
    function onLogout() {
        user = [];
        subjects = [];
        changeMonth(year, month);
        document.querySelector("#login").setAttribute("aria-hidden",false);
        document.querySelector("#login").classList.remove("hidden");
        document.querySelector("#logout").setAttribute("aria-hidden",true);
        document.querySelector("#logout").classList.add("hidden");
        document.querySelector("#view_by_subject").setAttribute("aria-hidden",true);
        document.querySelector("#view_by_subject").classList.add("hidden");
    }
    
    function onSubjectChange() {
        var subject = document.querySelector("#view_by_subject").value;
        if (subject == "todo") {
            subjects = user[0][1];
        } else {
            subjects = [subject];
        }
        changeMonth(year, month);
    }
    
    function onSearch() {
        var busqueda = document.querySelector("#busqueda").value;
        var found = false;
        for (i=0; i < events.length; i++) {
            if (events[i][1].indexOf(busqueda) != -1 && (subjects.length == 0 || subjects.indexOf(events[i][2][0]) != -1)) {
                document.querySelector("#day"+events[i][0]).focus();
                found = true;
                break;
            }
        }
        if (!found)
            alert("No se ha encontrado nada de lo que buscabas");
    }
    
    function prepareView(year, month) {
        // asignar número de dias del mes
        var days = daysInMonth(month, year);
        for (i=29; i<=31; i++) {
            if (days >= i) {
                document.querySelector("#day" + i).setAttribute("aria-hidden",false);
                document.querySelector("#day" + i).classList.remove("hidden");
            }
            else {
                document.querySelector("#day" + i).setAttribute("aria-hidden",true);
                document.querySelector("#day" + i).classList.add("hidden");
            }
        }
        
        // colocamos el primer dia del mes bajo el dia de la semana correcto
        var firstDay = firstDayOfMonth(month, year);
        for (i=1; i<=6; i++) {
            if (i < firstDay) {
                document.querySelector("#space" + i).setAttribute("aria-hidden",false);
                document.querySelector("#space" + i).classList.remove("hidden");
            }
            else {
                document.querySelector("#space" + i).setAttribute("aria-hidden",true);
                document.querySelector("#space" + i).classList.add("hidden");
            }
        }
        
        document.querySelector("#month").innerHTML = getMonthName(month) + " " + year;
    }
    
    function daysInMonth(month, year) {
        return new Date(year, month, 0).getDate();
        /* NOTA: la funcion date recibe month 0-11 pero en este caso le pasamos el mes siguiente, 
        y con day 0 obtenemos el ultimo dia del mes anterior.*/
    }
    
    function firstDayOfMonth(month, year) {
		var day = new Date(year, month-1, 1).getDay();
		if (day == 0) day = 7;
		return day;
	} 
	
	function getMonthName(month) {
	    var monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
	    return monthNames[month-1];
	}
	
	function showLoading () {
	    document.querySelector("img.loading").classList.remove("hidden");
	    document.querySelector("img.loading").setAttribute("aria-hidden",false);
	}
	
	function hideLoading () {
	    document.querySelector("img.loading").classList.add("hidden");
	    document.querySelector("img.loading").setAttribute("aria-hidden",true);
	}
	
	function clearDescription() {
	    var desc = document.querySelector("#event-description")
	    while(desc.hasChildNodes()){
            desc.removeChild(desc.lastChild);
        }
	}
}
