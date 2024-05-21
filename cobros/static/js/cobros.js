function __init()
{
    $('#search_input')
        .val('')
        .focus()
        .keyup(function(){

            if(!$.trim($(this).val()))
                $('.results .error').empty().hide();
        });

    var cache = {};
    $('#search_input').autocomplete({
        minLength: 0,
        select: function( event, ui ) {
            return false;
        },
        open: function() {
            $('.resultados .listSocios').html($(this).autocomplete("widget").html());
            $(this).autocomplete("widget").hide();
        },
        source: function( request, response ) {

        if (cache[request.term]) {
                response(cache[request.term]);
                return;
        }
        $("#listSocios").remove();
            $("#resultados").append("<tbody id=listSocios> </tbody>");
            console.log("pasa por remove listSocios")

            $.ajax({
                dataType : 'json',
                method : 'GET',
                url : '/configuracion/buscarSocio/',
                data : {
                    q : encodeURIComponent(request.term),
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
                },
                success : function(data) {
                    var socios = [];
                    console.log(data)
                    for(var x in data)
                    {
                        console.log(data[x].fields.numero)
                        socios.push({
                            
                            indice : x,
                            id : data[x].pk,
                            numero : data[x].fields.numero,
                            nombre : data[x].fields.persona[0],
                            apellido : data[x].fields.persona[1],
                            dni : data[x].fields.persona[2],
                        });
                    }
                    
                    cache[request.term] = socios;
                    response(socios);
                }
            });
        },
        response: function(event, ui) {

            if (ui.content.length === 0) {
                $('.results .error').html('No se encontraron resultados').show();
                $('.results .listSocios').empty();
            }
            else
                $('.results .error').empty().hide();
        }
    }).autocomplete('instance')._renderItem = function(table, item) {
        console.log("item:"+item.apellido)
        var user_tmpl = $('<tr />')
                        .addClass('tr');

        user_tmpl.append('<td>'+item.indice+'</td>');
        user_tmpl.append('<td>'+item.numero+'</td>');
        user_tmpl.append('<td>'+item.apellido+'</td>');
        user_tmpl.append('<td>'+item.nombre+'</td>');
        user_tmpl.append('<td collspan="3">'+'<a href="/cobros/verPagoSocio/'+item.id+'">Seleccionar</a>' +'</td>');

                        
        return $('#listSocios')
            .append(user_tmpl)
            
    };
}

