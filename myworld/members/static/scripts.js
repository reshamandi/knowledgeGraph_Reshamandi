$(document).ready(function() {
    $("#search").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("tbody tr").filter(function() {
            $(this).toggle($(this).text()
            .toLowerCase().indexOf(value) > -1)
        });
    });
});

function tran(){
    const x = document.getElementById('transSpec');
    const y = document.getElementById('productSpec')
    if(y.style.display === "block") y.style.display = "none";
    if(x.style.display === "none") x.style.display = "block";
}

function pdt(){
    const x = document.getElementById('productSpec')
    const y = document.getElementById('transSpec');
    if(y.style.display === "block") y.style.display = "none";
    if(x.style.display === "none") x.style.display = "block";
}