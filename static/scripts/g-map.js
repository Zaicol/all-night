let map, infoWindow;
let marlist = [];

function initMap() {
    let HTMLElement = document.getElementById("map");
    map = new google.maps.Map(HTMLElement, {
        styles: getMapStyle(),
        useStaticMap: false,
        center: {lat: 55.7522, lng: 37.6156},
        zoom: 12,
        mapTypeControl: false,
    });
    infoWindow = new google.maps.InfoWindow();
    addGPSButton();
    addAllButton();
    addNearButton();
    addCalendarButton();
    searchNear();
}

function addCalendarButton() {
    const mapButton = document.createElement("button");
    mapButton.id = "dp-btn";
    mapButton.innerHTML = "<img src='static/img/calendar.svg' alt='' style='filter: invert(1);'>";
    mapButton.classList.add("custom-map-control-button");
    /*mapButton.addEventListener("click", function () {

    }, {once: true});*/

    map.controls[google.maps.ControlPosition.TOP_LEFT].push(mapButton);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

window.addEventListener('load', async (event) => {
    console.log('page is fully loaded');
    let dp = $("#dp-btn");
    while (dp.length === 0) {
        await sleep(200);
        dp = $("#dp-btn");
        console.log(dp.length);
    }
    let ranged = new Datepicker('#dp-btn', {
        min: function () {
            let date = new Date();
            date.setDate(date.getDate());
            return date;
        },
        classNames: {
            node: 'datepicker custom'
        },
        onChange: function (date) {
            if (date) {
                searchdate = new Date(date);
                searchdate.given = true;
            }
        },
        i18n: {
            months: ["Январь", "Февраль", "Март", "Апрель",
                "Май", "Июнь", "Июль", "Август",
                "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
            weekdays: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]
        }
    });
});
