tab=document.getElementsByClassName("tab-content")


function opentab(arg){
    for(let t of tab){
        t.classList.remove('active-tab')

    }
    document.getElementById(arg).classList.add('active-tab')
}


const input = document.querySelector("#phone");
const ho=window.intlTelInput(input, {
  initialCountry: "np",
  strictMode: true,
  loadUtils: () => import("https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/25.2.1/build/js/utils.js") // for formatting/placeholders etc
});


document.getElementById("contactform").addEventListener("submit",function(e){
    if(ho.isValidNumber()){
        input.value=ho.getNumber();//full number 

    }
    else{
        e.preventDefault();
    }
})

