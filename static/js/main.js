var res = $('#result');
var loc = $('#location');
const owm_api_key = 'd1324848e943018b69d502b2e60c5174';

$(document).ready(function(){
    $('#fetch-data').click(()=>{
        fetchData();
    })

    $("#submit_data").click(function() {
        startLoader();
        var data = {
            temp: $("#temp").val(),
            rainfall: $("#rain").val(),
            ph:   $("#ph").val(),
            soil_type: $("#soil-type-select").val(),
            prev_crop: $("#prev-crop-select").val(),
        }
        console.log(data)
        $.ajax({
            method: "POST",
            url: "/api/get_predictions",
            data: data,
        }).done(function(data){
            if(data.success){
                showGraphs(data.result);
            }
            stopLoader();
        });
    });
});

function fetchData(){
    if (navigator.geolocation) {
        startLoader();
        navigator.geolocation.getCurrentPosition((position)=>{
            //$.post("/api/get_predictions", (data, status)=>{
                //console.log(data);
            //})
            $.get('https://geocode.xyz/'+position.coords.latitude.toFixed(5)+','+position.coords.longitude.toFixed(5)+'?geoit=json', (data, status)=>{
                loc.html("Latitude: "+position.coords.latitude+"<br/>Longitude: "+position.coords.longitude+"<br/>City: "+data.city)
                //console.log(data.city);

                $.get('https://history.openweathermap.org/data/2.5/aggregated/year?lat='+position.coords.latitude+'&lon='+position.coords.longitude+'&appid='+owm_api_key, (data, status)=>{
                    console.log(data)
                    stopLoader();
                })

            })
        });
    } else {
        alertiify.error("Geolocation is not supported by this browser.");
    }
}

function showGraphs(data){
    $("#result").css("display", "block");
    var labels = [];
    var totals = [];
    var temp = [];
    var rainfall = [];
    var ph = [];
    var soil = [];
    var prev = [];
    console.log(data);
    for(let x in data){
        labels.push(x);
        totals.push(data[x].total);
        temp.push(data[x].temp);
        rainfall.push(data[x].rainfall);
        ph.push(data[x].ph);
        soil.push(data[x].soil);
        prev.push(data[x].prev);
    }
    var back_colors = [
        'rgba(148, 74, 74, 0.2)',
        'rgba(116, 250, 175, 0.2)',
        'rgba(28, 79, 119, 0.2)',
        'rgba(233, 212, 99, 0.2)',
        'rgba(183, 7, 24, 0.2)',

        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',

        'rgba(154, 200, 153, 0.2)',
        'rgba(94, 79, 171, 0.2)',
        'rgba(50, 56, 22, 0.2)',
        'rgba(201, 48, 37, 0.2)',
    ]
    var border_colors = [
        'rgba(148, 74, 74, 1)',
        'rgba(116, 250, 175, 1)',
        'rgba(28, 79, 119, 1)',
        'rgba(233, 212, 99, 1)',
        'rgba(183, 7, 24, 1)',

        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',

        'rgba(154, 200, 153, 1)',
        'rgba(94, 79, 171, 1)',
        'rgba(50, 56, 22, 1)',
        'rgba(201, 48, 37, 1)',
    ]
    var total_ctx = document.getElementById('total-score').getContext('2d');
    var total_chart = new Chart(total_ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: totals,
                borderWidth: 1,
                backgroundColor: back_colors,
                borderColor: border_colors,
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Total Score'
            },
            legend: {
                display: false,
            }
        }
    });
    var temp_ctx = document.getElementById('temp-score').getContext('2d');
    var temp_chart = new Chart(temp_ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: temp,
                borderWidth: 1,
                backgroundColor: back_colors,
                borderColor: border_colors,
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Temperature Score'
            },
            legend: {
                display: false,
            }
        }
    });
    console.log(data)
    var rainfall_ctx = document.getElementById('rainfall-score').getContext('2d');
    var rain_chart = new Chart(rainfall_ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: rainfall,
                borderWidth: 1,
                backgroundColor: back_colors,
                borderColor: border_colors,
            }]
        },
        options:{
            title: {
                display: true,
                text: 'Rainfall Score'
            },
            legend: {
                display: false,
            }
        }
    });
    var ph_ctx = document.getElementById('ph-score').getContext('2d');
    var ph_chart = new Chart(ph_ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: ph,
                borderWidth: 1,
                backgroundColor: back_colors,
                borderColor: border_colors,
            }]
        },
        options:{
            title: {
                display: true,
                text: 'pH Score'
            },
            legend: {
                display: false,
            }
        }
    });
    var soil_ctx = document.getElementById('soil-score').getContext('2d');
    var soil_chart = new Chart(soil_ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: soil,
                borderWidth: 1,
                backgroundColor: back_colors,
                borderColor: border_colors,
            }]
        },
        options:{
            title: {
                display: true,
                text: 'Soil Score'
            },
            legend: {
                display: false,
            }
        }
    });
    var prev_ctx = document.getElementById('prev-crop-score').getContext('2d');
    var prev_chart = new Chart(prev_ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: prev,
                borderWidth: 1,
                backgroundColor: back_colors,
                borderColor: border_colors,
            }]
        },
        options:{
            title: {
                display: true,
                text: 'Previous Crop Score'
            },
            legend: {
                display: false,
            }
        }
    });
}

function getLocation() {

}

function startLoader(){
    $("#custom-loader").css('display', 'flex');
}
function stopLoader(){
    $("#custom-loader").css('display', 'none');
}
