$(document).ready(function () {
    $('#example').DataTable({
        pagingType: 'full_numbers',
    });
});

function toggle(ele){
    const divs = document.querySelectorAll('.query');
    for(let i = 0;i<divs.length;i++){
        divs[i].style.display = "none";
    }
    ele.style.display = "block";
}
