$('#busquedaSocio').keyup(function(e){
    consulta = $("#busquedaSocio").val();
    $.ajax({
    data: {'nombre': consulta},
    url: '/cobros/busquedaSocio/',
    type: 'get',
    success : function(data) {
            console.log(data[0]);
    },
    error : function(message) {
            console.log(message);
         }
    });
   });