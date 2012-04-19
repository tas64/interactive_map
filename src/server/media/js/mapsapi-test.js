window.G_ID = "#maps-api-testerfield";

function evaluate_this() {
    eval( $(G_ID).val());
}

function on_init_map() {
    $(G_ID).val(
"window.myMap = new ymaps.Map('myMap', { \n\
// При инициализации карты, обязательно нужно указать \n\
// ее центр и коэффициент масштабирования \n\
    center: [55.76, 37.64], // Москва \n\
    zoom: 10 \n\
});");
}

function on_pan_to() {
$(G_ID).val(
"destinations = { \n\
    'Москва': [55.753559, 37.609218], \n\
    'Санкт-Петербург': [59.93853, 30.313497], \n\
    'Екатеринбург': [56.829748, 60.617435], \n\
    'Одесса': [46.466444, 30.7058] \n\
}; \n\
\n\
var geoPoint = destinations['Санкт-Петербург']; \n\
\n\
window.myMap.panTo(geoPoint, { flying: true, duration: 3000 });");
}

function on_delete() {
    $(G_ID).val("window.myMap.destroy();");
}

function on_add_points() {
    $(G_ID).val(
    "var myPlacemark = new ymaps.Placemark([55.76, 37.64], \n\
        { iconContent: 'Щелкни по мне', \n\
            balloonContentHeader: 'Заголовок', \n\
            balloonContentBody: 'Содержимое <em>baloon</em>', \n\
            balloonContentFooter: 'Подвал'}, \n\
        { preset: 'twirl#blueStretchyIcon' }); \n\
window.myMap.geoObjects.add(myPlacemark); \n\
\n\
var myGeoObject = new ymaps.GeoObject({ geometry: { type: 'Point' ,coordinates: [55.7, 37.6] }}) \n\
window.myMap.geoObjects.add(myGeoObject);");
}

function on_add_route() {
    $(G_ID).val(
    "ymaps.route([ \n\
        'Москва, метро Смоленская', \n\
        { \n\
            type: 'viaPoint', \n\
            point: 'Москва, метро Арбатская' \n\
        }, \n\
        [55.74062, 37.62561] \n\
    ], { \n\
        mapStateAutoApply: true \n\
    }).then(function (route) { \n\
            myMap.geoObjects.add(route); \n\
        }, function (error) { \n\
            alert('Возникла ошибка: ' + error.message); \n\
        }); \n\
\n\
//пояснения: \n\
// Прокладывание маршрута от станции метро 'Смоленская' \n\
// до станции Третьяковская (маршрут должен проходить через метро 'Арбатская'). \n\
// Точки маршрута можно задавать 3 способами:  как строка, как объект или как массив геокоординат. \n\
// ymaps.route([ \n\
//     'Москва, метро Смоленская', \n\
//     { \n\
//         type: 'viaPoint', // метро арбатская - транзитная точка (проезжать через эту точку, но не останавливаться в ней) \n\
//         point: 'Москва, метро Арбатская' \n\
//     }, \n\
//     [55.74062, 37.62561] // метро 'Третьяковская' \n\
// ], { \n\
//     // Опции маршрутизатора \n\
//     mapStateAutoApply: true // автоматически позиционировать карту \n\
// }).then(function (route) { \n\
//     myMap.geoObjects.add(route); \n\
// }, function (error) { \n\
//     alert('Возникла ошибка: ' + error.message); \n\
// });");

}

function on_add_polyline() {
    $(G_ID).val(
"var  myPolyline = new ymaps.Polyline([ \n\
        // Координаты вершин ломаной. \n\
        [55.80, 37.60], \n\
        [55.80, 37.50], \n\
        [55.70, 37.40], \n\
        [55.70, 37.50] \n\
    ], {}, { \n\
        strokeWidth: 5 // ширина линии \n\
    }); \n\
    myMap.geoObjects.add(myPolyline);");
}