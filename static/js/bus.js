document.addEventListener('DOMContentLoaded', function() {
var flag=0;
const documentButton=document.querySelector('#busBT');
const busButton =() => {
    if (flag===0) {
        document.querySelector('#goTo').textContent='八王子行き';
        document.querySelector('.bus-times span').innerText='08:00';
        document.querySelector('#bus').style = "transform: scale(-1, 1);"
        flag=1;
    } else {
        document.querySelector('#goTo').textContent='キャンパス行き';
        document.querySelector('.bus-times span').innerText='15:00';
        document.querySelector('#bus').style = ""
        flag=0;
    }
};
documentButton.addEventListener('click',busButton);
console.log(documentButton.value);
});
