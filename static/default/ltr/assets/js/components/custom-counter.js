// Circle

// var value = $('.c-counter1').text();
var value = "5000";
$('.c-counter1').countTo({
    from: 0,
    to: value,
    speed: cSpeed,
    formatter: function (value, options) {
        return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
    }
});
var value = $('.c-counter2').text();
$('.c-counter2').countTo({
    from: 0,
    to: value,
    speed: cSpeed,
    formatter: function (value, options) {
        return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
    }
});
var value = $('.c-counter3').text();
$('.c-counter3').countTo({
    from: 0,
    to: value,
    speed: cSpeed,
    formatter: function (value, options) {
        return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
    }
});
var value = $('.c-counter4').text();
$('.c-counter4').countTo({
    from: 0,
    to: value,
    speed: cSpeed,
    formatter: function (value, options) {
        return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
    }
});