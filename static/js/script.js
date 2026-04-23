function mostrarCampos(){
    let campo_estudiante = document.getElementById('estudiante')
    let campo_profesor = document.getElementById('profesor')

    campo_estudiante.style.display = 'none'
    campo_profesor.style.display = 'none'

    if(document.getElementById('tipo_estudiante').checked){
        campo_estudiante.style.display = 'block'
    } else if(document.getElementById('tipo_profesor').checked){
        campo_profesor.style.display = 'block'
    }

}