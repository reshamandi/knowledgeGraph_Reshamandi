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