document.addEventListener('DOMContentLoaded',function(){

    let show_password = document.querySelector('#show_password');
    let password = document.querySelector('#password');
    let confirm = document.querySelector('#confirm');
    show_password.onclick = function(){
        if (password.type === "password"){
            password.type = "text";
            confirm.type = 'text';

        } else {
            password.type = 'password';
            confirm.type = 'password';
        }
    }
});