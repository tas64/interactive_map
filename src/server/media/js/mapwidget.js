ymaps.ready(init);

function getCurCoords() {
    var latitude = $("#id_latitude").val();
    var longitude = $("#id_longitude").val();
    if (latitude == "" || longitude == "") {
        return undefined;
    }
    return [latitude, longitude];
}

function panTo() {
    var coords = getCurCoords();
    if (coords == undefined) {
        return;
    }
    window.myMap.balloon.close();
//    window.myMap.panTo(coords, {
//        flying: true,
//        duration: 0
//    });
    openBaloon(coords);

}

function openBaloon(coords) {
    var name = $("#id_name").val();
    //alert('change name to ' + name)
    window.myMap.balloon.open(coords, ({contentHeader: name}));
    window.myMap.baloon.autoPan();
}

function init () {
    var initCoords = getCurCoords();
    if (initCoords == undefined) {
        initCoords = [59.93853, 30.313497]; // Питер
    }
    window.myMap = new ymaps.Map('myMap', {
        center: initCoords,
        zoom: 13
    });
    window.myMap.controls.add('zoomControl');

    window.myMap.events.add('click', function (e) {
        //if (!window.myMap.balloon.isOpen()) {
            var coords = e.get('coordPosition');
            openBaloon(coords)
            $("#id_latitude").val(coords[0].toPrecision(6));
            $("#id_longitude").val(coords[1].toPrecision(6));
    });

    $("#id_latitude").bind('change', panTo);
    $("#id_name").bind('keyup', openBaloon);
    $("#id_longitude").bind('change', panTo);

    panTo();
}


