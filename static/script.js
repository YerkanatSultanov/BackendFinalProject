let offset = 0;
const sliderLine = document.querySelector('.slider-line');

document.querySelector('.slider-next').addEventListener('click', function(){
    offset += 306;
    if(offset >= 1224){
        offset = 0;
    }
    sliderLine.style.left = -offset + 'px';
})
