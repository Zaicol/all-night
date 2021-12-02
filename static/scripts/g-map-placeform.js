let map, infoWindow;
let marlist = [];

function initMap() {
    let HTMLElement = document.getElementById("map");
    map = new google.maps.Map(HTMLElement, {
        styles: getMapStyle(),
        useStaticMap: false,
        center: {lat: 55.7522, lng: 37.6156},
        zoom: 12,
    });
    infoWindow = new google.maps.InfoWindow();
    addGPSButton();
}

document.getElementById('search-button').addEventListener(
    'click', async function (e) {
        e.preventDefault();
        const s = document.getElementById('search');
        const query = s.value;
        console.log(query);
        const response = await fetch(
            `https://maps.googleapis.com/maps/api/geocode/json?address=${query}&sensor=false&language=ru&key=AIzaSyA0qB_bzyxdUXulSX0-N3K9oRwkxvmW32g`
        );
        let res = await response.json()
        if (res != null && res !== [] && res["status"] === "OK" && res["results"]) {
            let position = searchSuccess(res)[0];
            document.getElementById('lat').value = position['lat'];
            document.getElementById('lon').value = position['lng'];
        } else {
            document.getElementById("place-not-found").classList.remove('d-none');
        }
        return false;
    });

document.getElementById('search-latlon-button').addEventListener(
    'click', async function (e) {
        e.preventDefault();
        const lat = document.getElementById('lat').value;
        const lon = document.getElementById('lon').value;
        const response = await fetch(
            `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lon}&sensor=false&language=ru&key=AIzaSyA0qB_bzyxdUXulSX0-N3K9oRwkxvmW32g`
        );
        let res = await response.json()
        if (res != null && res !== [] && res["status"] === "OK" && res["results"]) {
            document.getElementById('search').value = searchSuccess(res)[1];
        } else {
            document.getElementById("place-not-found").classList.remove('d-none');
        }
        return false;
    });

function searchSuccess(res) {
    document.getElementById("place-not-found").classList.add('d-none');
    console.log(res);
    const {lat, lng} = res["results"][0]["geometry"]["location"];
    const display_name = res["results"][0]["formatted_address"];
    const position = {lat: +lat, lng: +lng};
    getMap([position], [`${display_name}`]);
    return [position, display_name];
}