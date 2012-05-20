ymaps.ready(init);

function init () {
    window.myMap = new ymaps.Map('myMap', {
        center: [59.93853, 30.313497], // Питер
        zoom: 12
    });
    window.myMap.controls.add('zoomControl');
}

function clear_all_placemarks() {
    if (window.immobile_placemarks != undefined) {
        $.each(window.immobile_placemarks, function(key, placemark) {
           window.myMap.geoObjects.remove(placemark);
        });
    }
    window.immobile_placemarks = {};
}

function immobile_click(id) {
    if (window.immobile_placemarks[id] != undefined) {
        var placemark = window.immobile_placemarks[id];
        window.myMap.geoObjects.remove(placemark);
        delete window.immobile_placemarks[id];
        return;
    }
    var immobile = window.immobiles[id];
    var geoCoords = [immobile.latitude, immobile.longitude];
    var myPlacemark = new ymaps.Placemark(geoCoords,
            { iconContent: immobile.name,
              balloonContentHeader: immobile.name,
              balloonContentBody: 'Телефон <em>' + immobile.phone + '</em>',
              balloonContentFooter:  '['+immobile.latitude +','+immobile.longitude+']'},
            { preset: 'twirl#blueStretchyIcon' });
    window.immobile_placemarks[id] = myPlacemark;
    window.myMap.geoObjects.add(myPlacemark);
}

function clear_movable_path() {
    if (window.movable_showed_id != undefined) {
        window.myMap.geoObjects.remove(window.movable_polyline);
        window.movable_showed_id = undefined;
    }
}

function movables_click(id) {

    if (window.movable_showed_id == id) {
        return;
    }

    clear_movable_path();

    $.getJSON('/ajax/location_points/' + id +'/', function(data) {
        var points = [];
        $.each(data, function(key,value) {
            points.push([value.latitude, value.longitude])
        });
        if (points.length == 0) {
            return;
        }
        window.movable_showed_id = id;

        var properties = {};
        var options = {
            //draggable: true,
            //strokeColor: '#000000',
            strokeWidth: 2
            //strokeStyle: '1 5'
        };
        window.movable_polyline = new ymaps.Polyline(points, properties, options);
        window.myMap.geoObjects.add(window.movable_polyline);
        //window.myMap.panTo(points[0], { flying: true, duration: 1000 });
        window.myMap.setBounds(window.movable_polyline.geometry.getBounds(), { checkZoomRange: true });
    });
}

function search_immobile() {
    var text = $('#immobiles_search').val();

    if (text == "") {
        return;
    }

    clear_all_placemarks();

    $.getJSON('/ajax/immobile/?q=' + text, function(data) {
        window.immobiles = data;
        $('#immobiles_container').html("");
        $.each(data, function(key,value) {
            var items = [];
            $.each(data, function(key,value) {
                items.push("<input type='checkbox' onchange='immobile_click(" + key +")'/>" + value.name);
            });
            $('#immobiles_container').html(items.join('<br/>'));
        });

    });

}

function search_movables() {
    var text = $('#movables_search').val();

    if (text == "") {
        return;
    }

    clear_movable_path();

    $.getJSON('/ajax/movables/?q=' + text, function(data) {
        window.globalData = data;
        $('#movables_container').html("");
        $.each(data, function(key,value) {
            var items = [];
            $.each(data, function(key,value) {
                items.push("<input type='radio' name='movables_radio' onclick='movables_click(" + value.id +")'/>" + value.name);
            });
            $('#movables_container').html(items.join('<br/>'));
        });

    })

}

