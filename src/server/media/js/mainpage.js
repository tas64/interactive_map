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
        clear_route();
        clear_baloons();
    }
    window.movable_showed_id = undefined;
    $("#slider").addClass('hide');
}

function movables_click(id) {

    if (window.movable_showed_id == id) {
        return;
    }

    clear_movable_path();

    $.getJSON('/ajax/location_points/' + id +'/', function(data) {

        window.location_points = data;
        window.movable_showed_id = id;

        paintRoute(data);
        paintBaloons(data);

        window.myMap.setBounds(window.movable_polyline.geometry.getBounds(), { checkZoomRange: true });
        $("#slider").removeClass("hide");

        var first = data[0].hour*60 + data[0].minute;
        var second = data[data.length-1].hour * 60 + data[data.length-1].minute;
        set_fields(first, second)

        $( "#slider-range" ).slider( "option", "values", [first,second] );


    });
}

function paintRoute(data) {
    clear_route();
    var points = [];
    $.each(data, function(key,value) {
        points.push([value.latitude, value.longitude])
    });
    if (points.length == 0) {
        return;
    }
    var properties = {};
    var options = {
        //draggable: true,
        //strokeColor: '#000000',
        strokeWidth: 2
        //strokeStyle: '1 5'
    };
    window.movable_polyline = new ymaps.Polyline(points, properties, options);
    window.myMap.geoObjects.add(window.movable_polyline);

}

function paintBaloons(data) {
    clear_baloons();
    var points = [];
    $.each(data, function(key,value) {
        var point = [value.latitude, value.longitude];
        var myPlacemark = new ymaps.Placemark(point,
            { iconContent: value.hour+":"+value.minute+":"+value.second},
            { preset: 'twirl#blueStretchyIcon' });
        window.movable_placemarks.push(myPlacemark);
        window.myMap.geoObjects.add(myPlacemark);

    });
}

function clear_route() {
    if (window.movable_polyline == undefined) {
        return;
    }
    window.myMap.geoObjects.remove(window.movable_polyline);
}

function clear_baloons() {
    if (window.movable_placemarks == undefined) {
        window.movable_placemarks = [];
    }
    $.each(window.movable_placemarks, function(key, placemark) {
        window.myMap.geoObjects.remove(placemark);
    });
    window.movable_placemarks = [];
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

function minutes_to_fulltime(time) {
    var minutes = time % 60;
    var hours = (time - minutes)/60;
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    if (hours < 10) {
        hours = "0" + hours;
    }
    return hours + ":" + minutes;
}

function set_fields(left, right) {
    $(".left-timefield").html( minutes_to_fulltime(left));
    $(".right-timefield").html( minutes_to_fulltime(right));
}

$(function() {
    $( "#slider-range" ).slider({
        range: true,
        min: 0,
        max: 1440,
        values: [ 0, 1440 ],
        slide: function( event, ui ) {
            //$( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
            set_fields(ui.values[0], ui.values[1]);
            show_only_points(ui.values[0], ui.values[1]);
        }
    });
    set_fields($( "#slider-range" ).slider( "values", 0), $( "#slider-range" ).slider( "values", 1 ));
});

function show_only_points(time_left, time_right) {

    if (window.location_points == undefined) {
        return;
    }

    var minutes_left = time_left % 60;
    var hours_left = (time_left - minutes_left)/60;

    var minutes_right = time_right % 60;
    var hours_right = (time_right - minutes_right)/60;

    filtered = window.location_points.filter( function(val) {
        if (val.hour > hours_left && val.hour < hours_right) {
            return true;
        }
        if (val.hour == hours_left && val.minute >= minutes_left) {
            return true;
        }
        if (val.hour == hours_right && val.minute <= minutes_right) {
            return true;
        }
        return false;
    });

    paintRoute(filtered);
    paintBaloons(filtered);

}

function enterHandling(who, func) {
    $(who).keydown(function(e) {
        if (e.keyCode == 13) {
            func();
        }
    });
}

window.onload = function() {
    enterHandling('#movables_search', search_movables);
    enterHandling('#immobiles_search', search_immobile);
}