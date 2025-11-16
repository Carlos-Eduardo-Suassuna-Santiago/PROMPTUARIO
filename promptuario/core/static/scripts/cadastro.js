 const selectTipo = document.getElementById('tipo_conta');
 const campoCRM = document.getElementById('campo_medico');
 const campoCRT = document.getElementById('campo_funcionario');

 selectTipo.addEventListener('change', function() {
    if (this.value === "medico") {
        campoCRM.style.display = "block"; 
        campoCRT.style.display = "none";    
    } else if (this.value === "funcionario")  { 
        campoCRM.style.display = "none"; 
        campoCRT.style.display = "block"; 
    } else {
        campoCRM.style.display = "none";
        campoCRT.style.display = "none";    
    }
 });
