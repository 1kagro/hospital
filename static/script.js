console.log("hola");
checkpass();

function checkpass() {
    let pass = select_id('pass').value;
    let pass2 = select_id('pass2').value;

    console.log("pass: " + pass + " Pass2: " + pass2);
    if (pass != pass2) {
        alert("Las contraseñas no coinciden, intente nuevamente")
    }
}

function select_id(id) {
    return document.getElementById(id);
}

function select_class(clas) {
    return document.querySelector(clas);
}