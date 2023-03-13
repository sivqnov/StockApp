let checkBox = document.getElementById("passwordInputCheckbox");
var input = document.getElementsByClassName("passwordInput")

document.addEventListener('click',(e) =>
    {
        let elementID = e.target.id;
        if(elementID == "passwordInputCheckbox"){
            if(checkBox.checked == true){
                for(let i=0;i<input.length;i++){
                    input[i].type = "text";
                }
            }
            else{
                for(let i=0;i<input.length;i++){
                    input[i].type = "password";
                }
            }
        }
    }
);