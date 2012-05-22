ymaps.ready(init);

function init () {
    window.myMap = new ymaps.Map("map", {
            center: [59.93853, 30.313497],
            zoom: 10
        });
    window.myMap.controls.add('zoomControl');
}

var STATUS = {
    NO_WAY : 0,
    SAVED_WAY : 1,
    EDITING : 2
}


function set_status(status) {
    window.my_status = status;
    if (status == STATUS.NO_WAY) {
        $('#help').html("Перетаскивая точки линии, задайте путь для подвижного объекта");
        $('#set-time-button').prop("disabled", false);
        $('#del-time-button').prop("disabled", true);
        $("#save-time-button").prop("disabled", true);

        clear_placemarks();

        points = [
            [59.9400, 30.3100 ],
            [59.9332, 30.2912 ]
        ];
        show_init_line(points);

        window.geoobject.editor.startEditing();
    } else if (status == STATUS.SAVED_WAY) {
        $('#help').html("На карте показан созданный путь. Если хотите создать новый, то удалите текущий путь, нажав 'удалить путь'");

        clear_placemarks();
        var points = [];
        $.each(window.globalData, function(key,value) {
            var point = [value.latitude, value.longitude];
            points.push(point);

            var myPlacemark = new ymaps.Placemark(point,
                { iconContent: value.hour+":"+value.minute+":"+value.second},
                { preset: 'twirl#blueStretchyIcon' });
            window.placemarks.push(myPlacemark);
            window.myMap.geoObjects.add(myPlacemark);

        });
        show_init_line(points);
        fill_table(window.globalData);
        window.geoobject.editor.stopEditing();
        $('#set-time-button').prop("disabled", true);
        $('#del-time-button').prop("disabled", false);
        $("#save-time-button").prop("disabled", true);
    } else if (status == STATUS.EDITING) {
        clear_placemarks();
        $('#help').html("Введите время для каждой точки, затем нажмите на кнопку 'Сохранить'");
        $('#set-time-button').prop("disabled", true);
        $('#del-time-button').prop("disabled", true);
        $("#save-time-button").prop("disabled", false);
        window.geoobject.editor.stopEditing();

        var coords = window.geoobject.geometry.getCoordinates();
        window.globalEditingData = [];


        $.each(coords, function(key,value) {
            window.globalEditingData.push( {'latitude' : value[0].toPrecision(6), 'longitude' : value[1].toPrecision(6),
                                               'hour' : '', 'minute' : '', 'second' : '0'});
        });

        fill_table_editing(window.globalEditingData);
    } else {
        $('#help').html("");
    }
}

function clear_placemarks() {
    if (window.placemarks == undefined) {
        window.placemarks = [];
    }
    $.each(window.placemarks, function(key, placemark) {
        window.myMap.geoObjects.remove(placemark);
    });
    window.placemarks = [];
}

function init_path(id) {

    //set_status(undefined);

    $.getJSON('/ajax/location_points/' + id + '/', function(data) {

        window.globalData = data;
        window.globalId = id;

        if (data.length == 0) {
            set_status(STATUS.NO_WAY);
        } else {
            set_status(STATUS.SAVED_WAY);
        }

    });
}


function fill_table(data) {
    clear_table();

    var TD = "<td>";
    var _TD = "</td>";
    var TR = "<tr>";
    var _TR = "</tr>";
    var SEP = _TD + TD;
    var items = [];

    $.each(data, function(key,value) {
        items.push(TR + TD+value.latitude.toPrecision(6) + SEP + value.longitude.toPrecision(6) +SEP
            +value.hour+ SEP + value.minute + SEP +  value.second + _TD);
    });
    $('#time table ').append(items.join(' '));
}

function fill_table_editing(data) {

    clear_table();
    var TD = "<td>";
    var _TD = "</td>";
    var TR = "<tr>";
    var _TR = "</tr>";
    var SEP = _TD + TD;
    var items = [];
    $.each(data, function(key,value) {
        var hour_field = "<input type='text' onchange='change_hour(" + key + ", $(this).val())' onclick='show_object(" + key + ")' class='hour field'/>";
        var minute_field = "<input type='text' onchange='change_minute(" + key + ",$(this).val())' onclick='show_object(" + key + ")' class='minute field'/>";
        var second_field = "<input type='text' onchange='change_second(" + key + ",$(this).val())' onclick='show_object(" + key + ")' class='second field' value='0'/>";
        items.push(TR + TD+value.latitude + SEP + value.longitude +SEP  +hour_field+ SEP + minute_field + SEP + second_field + _TD);
    });
    $('#time table ').append(items.join(' '));
}

function show_object(id) {
    var coords = [window.globalEditingData[id].latitude, window.globalEditingData[id].longitude];
    window.myMap.balloon.open(coords, ({contentHeader: coords }));
}



function show_init_line(points) {

    var myGeometry = {
        type: 'LineString',
        coordinates: points
    };
    var myOptions = {
        strokeWidth: 6,
        strokeColor: '#0000FF'
        //draggable: true
    };

    window.geoobject = new ymaps.GeoObject({geometry: myGeometry}, myOptions);
    window.myMap.geoObjects.add(window.geoobject);
    window.myMap.setBounds( window.geoobject.geometry.getBounds(), { checkZoomRange: true });

}

function set_time(){
    set_status(STATUS.EDITING);
}

function delete_way() {
    $.getJSON('/ajax/del_location_points/' + window.globalId + '/', function(data) {
        window.myMap.geoObjects.remove(window.geoobject);
        set_status(STATUS.NO_WAY);
        clear_table();

    });
}

function save_way() {
    var json_data = JSON.stringify(window.globalEditingData);
    $.getJSON('/ajax/save_location_points/' + window.globalId + '/',
        {data : json_data },
        function(data) {
        if (data.result != 'OK') {
            alert('Ошибка в отправляемых данных. Возможно, не все данные заполнены, или заполнены неправильно.');
        } else {
            window.location.reload(true);
        }
    });
}

function change_hour(id,value) {
    window.globalEditingData[id].hour = value;
}

function change_minute(id,value) {
    window.globalEditingData[id].minute = value;
}

function change_second(id,value) {
    window.globalEditingData[id].second = value;
}


function clear_table() {
    $('#time table tr:not(.header)').remove();
}

