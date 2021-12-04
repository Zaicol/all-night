let searchdate = new Date;
searchdate.given = false;

function getMap(position, tooltip) {
    if (marlist) {
        for (let i = 0; i < marlist.length; i++) {
            marlist[i].setMap(null);
            marlist[i] = null;
        }
        marlist = [];
    }
    for (let i = 0; i < position.length; i++) {
        try {
            marlist.push(new google.maps.Marker({
                position: position[i],
                map: map,
                animation: google.maps.Animation.DROP
            }));
            makeInfoWindowEvent(map, infoWindow, tooltip[i], marlist[marlist.length - 1])
        } catch (err) {
            console.log(err);
            console.log(typeof position[i][0]);
        }
    }
    map.setCenter(position[position.length - 1]);
}

function addGPSButton() {
    const locationButton = document.createElement("button");

    locationButton.innerHTML = "<img src='static/img/gps.png' alt=''>";
    locationButton.classList.add("custom-map-control-button");
    locationButton.addEventListener('click', function (e) {
        e.preventDefault();
    });
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(locationButton);
    locationButton.addEventListener("click", () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    getMap([pos], ['Вы']);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

function addAllButton() {
    const locationButton = document.createElement("button");

    locationButton.textContent = "Все";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(locationButton);
    locationButton.addEventListener("click", showAllPlaces);
}

async function showAllPlaces() {
    let addresses = await getAllPlaces();
    console.log(addresses);
    let position = [];
    let tooltip = [];
    let place;
    for (let i = 0; i < addresses.length; i++) {
        place = addresses[i];
        let a = `${place["title"]} · `;
        a += `<a target="_blank" rel="noopener noreferrer" href="${place["content"]}">${place["shortlink"]}</a>`;
        a += `<br><img src="${place["pic"]}" alt="">`;
        position.push({lat: +place["lat"], lng: +place["lon"]});
        tooltip.push(a);
    }
    getMap(position, tooltip);
}

async function getAllPlaces() {
    let postdata;
    if (searchdate.given) {
        let y = searchdate.getFullYear();
        let m = searchdate.getMonth() + 1;
        let d = searchdate.getDate();
        postdata = `?date=${y},${m},${d}`
    } else {
        postdata = ''
    }
    const response = await fetch("./api/places/all" + postdata);
    return await response.json();
}

function addNearButton() {
    const locationButton = document.createElement("button");

    locationButton.textContent = "Рядом";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(locationButton);
    locationButton.addEventListener("click", searchNear);
}

function searchNear() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            coordcalc,
            () => {
                handleLocationError(true, infoWindow, map.getCenter());
            }
        );
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

async function coordcalc({coords}) {
    const km = document.getElementById('km').value;
    const {latitude, longitude} = coords;
    const currentPosition = {lat: +latitude, lng: +longitude};
    let addresses = await getAllPlaces();
    let position = [];
    let tooltip = [];
    let d;
    let dconv;
    for (let i = 0; i < addresses.length; i++) {
        const {title, content, shortlink, lat, lon, pic} = addresses[i];
        d = getDistanceFromLatLonInKm(latitude, longitude, lat, lon);
        if (d < km) {

            if (d < 1) {
                dconv = (d * 1000).toFixed() + ' м';
            } else {
                dconv = d.toFixed(1) + ' км';
            }

            position.push({lat: +lat, lng: +lon});
            tooltip.push(`${title} · <a target="_blank" rel="noopener noreferrer" href="${content}">${shortlink}</a> · ${dconv}<br><img src="${pic}" alt="">`);
        }

    }
    position.push(currentPosition);
    tooltip.push("Вы");
    console.log([position, tooltip]);
    getMap(position, tooltip);
}

function deg2rad(degrees) {
    return degrees * (Math.PI / 180);
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the earth in km
    const dLat = deg2rad(lat2 - lat1);  // deg2rad below
    const dLon = deg2rad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)
    ;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function getMapStyle() {
    styles = [
        {
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#212121"
                }
            ]
        },
        {
            "elementType": "labels.icon",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#757575"
                }
            ]
        },
        {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#212121"
                }
            ]
        },
        {
            "featureType": "administrative",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#757575"
                }
            ]
        },
        {
            "featureType": "administrative.country",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#9e9e9e"
                }
            ]
        },
        {
            "featureType": "administrative.land_parcel",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "administrative.locality",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#bdbdbd"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#757575"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#181818"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#616161"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#1b1b1b"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "geometry.fill",
            "stylers": [
                {
                    "color": "#2c2c2c"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#8a8a8a"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#373737"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#3c3c3c"
                }
            ]
        },
        {
            "featureType": "road.highway.controlled_access",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#4e4e4e"
                }
            ]
        },
        {
            "featureType": "road.local",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#616161"
                }
            ]
        },
        {
            "featureType": "transit",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#757575"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#000000"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#3d3d3d"
                }
            ]
        }
    ];
    return styles;
}

function makeInfoWindowEvent(map, infowindow, contentString, marker) {
    google.maps.event.addListener(marker, 'click', function () {
        content = "<div id='popup'>" + contentString + "</div>"
        infowindow.setContent(content);
        infowindow.open(map, marker);
    });
}