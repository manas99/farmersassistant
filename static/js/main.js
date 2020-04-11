var res = $('#result');
$(document).ready(function(){
    //var res = $('#result');
    $('#pred-button').click(()=>{
        getLocation();
    })

    $( "#submit_data" ).click(function() {
        var temp = $("#temp").val();
        var rain = $("#rain").val();
        var ph =   $("#ph").val();
        var soil = $("#soil").val();
        var previous_crop = $("#crop").val();

        $.post( "/api/get_predictions", { temp: temp, rainfall:rain, ph:ph, soil_type:soil, prev_crop:previous_crop} , function(data){
        console.log(data);

        } );
});

})

function getLocation() {
    if (navigator.geolocation) {
        startLoader();
        navigator.geolocation.getCurrentPosition((position)=>{
            //$.post("/api/get_predictions", (data, status)=>{
                //console.log(data);
            //})
            $.get('https://geocode.xyz/'+position.coords.latitude.toFixed(5)+','+position.coords.longitude.toFixed(5)+'?geoit=json', (data, status)=>{
                console.log(data.city);
                res.html("Latitude: "+position.coords.latitude+"<br/>Longitude: "+position.coords.longitude+"<br/>City: "+data.city)
                stopLoader();
            })
        });
    } else {
        alertiify.error("Geolocation is not supported by this browser.");
    }
}

function startLoader(){
    $("#custom-loader").css('display', 'flex');
}
function stopLoader(){
    $("#custom-loader").css('display', 'none');
}


