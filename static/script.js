let offset = 0;
let num = 0;
const sliderLine = document.querySelector('.slider-line');

document.querySelector('.slider-next').addEventListener('click', function(){
    offset += 240;
    var slides = document.getElementsByClassName('borders');
    num += 1;
    if(slides.length === num){
        num = 0;
        offset = 0;
    }
    sliderLine.style.left = -offset + 'px';
})


window.addEventListener('click', function(event) {
  var dropdowns = document.getElementsByClassName('dropdown-content');
  for (var i = 0; i < dropdowns.length; i++) {
    var dropdown = dropdowns[i];
    if (!event.target.matches('.dropdown-btn') && !dropdown.contains(event.target)) {
      dropdown.style.display = 'none';
    }
  }
});

