console.log("hola");

function checkpass() {
    let pass = select_id('pass').value;
    let pass2 = select_id('pass2').value;

    console.log("pass: " + pass + " Pass2: " + pass2);
    if (pass != pass2) {
        alert("Las contraseñas no coinciden, intente nuevamente")
    }
}

function checkUserPass() {
    let user_id = select_id('id').value;
    let password = select_id('pass').value;
    if (user_id == 123) {
        console.log("a")
        window.location.href = '../templates/dashboard.html'
    }
}


function select_id(id) {
    return document.getElementById(id);
}

function select_class(clas) {
    return document.querySelector(clas);
}