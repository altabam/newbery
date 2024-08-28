
function __init() {
    $('#search_input')/* inicializamos el buscador */
        .val('')
        .focus()
        .keyup(function() {
            if (!$.trim($(this).val())) {
                $('#listSocios .error').empty().hide();
            }
        });

    var cache = {};
    $('#search_input').autocomplete({ /* configuracion de autocompletado incluso sin tener min */
        minLength: 0,
        select: function(event, ui) {
            return false;  // Previene que se seleccione automáticamente
        },
        open: function() {
            $('#listSocios').html($(this).autocomplete("widget").html());
            $(this).autocomplete("widget").hide();
        },
        source: function(request, response) {/* Busca el termino de busqueda en cache */
            if (cache[request.term]) {
                console.log("request.term"+cache[request.term]);
                response(cache[request.term]);
                return;
            }

            // Agregue esto para: Asegurar que el contenedor de resultados esté vacío antes de agregar nuevos resultados
           // $("#listSocios").empty();
            //$("#resultados").append("<tbody id='listSocios'></tbody>");
            

            $.ajax({ /* Si no está en cache, hace una peticion con ajax */
                dataType: 'json',
                method: 'GET',
                url: '/configuracion/buscarSocioResponsable/',
                data: {  /* le envia el termino de busqueda con un codigo por seguridad */
                    q: encodeURIComponent(request.term),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(data) {
                    var socios = [];
                    console.log(data);
                    for (var x in data) {
                        console.log(data[x].fields.numero);
                        socios.push({
                            indice: x,
                            id: data[x].pk,
                            numero: data[x].fields.numero,
                            nombre: data[x].fields.persona[0],
                            apellido: data[x].fields.persona[1],
                            dni: data[x].fields.persona[2],
                        });
                    }
                    
                   
                    cache[request.term] = socios;
                    response(socios);
                }
            });
        },
        response: function(event, ui) {
//            console.log("ui.content");
  //          console.log(ui.content);
    //        console.log(ui.content.length);
            if (!ui.content.length) {
              //  $('.resultados .error').html('No se encontraron resultados').show();
      //          console.log("ui.contente remove");
                $('#listSocios').empty();
            } else {
//                $('.resultados .error').empty().hide();
       //         console.log("pasa por ui.content mayos que vacio")
            }
        }
    }).autocomplete('instance')._renderItem = function(table, item) {
        console.log("item:" + item.apellido);
        var user_tmpl = $('<tr />')
                        .addClass('tr');

        user_tmpl.append('<td>' + item.indice + '</td>');
        user_tmpl.append('<td class="tdNumero">' + item.numero + '</td>');
        user_tmpl.append('<td class="tdNumero">' + item.dni + '</td>');
        user_tmpl.append('<td class="td-nombre">' + item.apellido + '</td>');
        user_tmpl.append('<td class="td-nombre">' + item.nombre + '</td>');
        user_tmpl.append('<td class="td-opciones" colspan="3">' +
                         '<div class="divBoton">' +
                         '<a class="boton-editar" href="/configuracion/listarIntegrantesSocios/' + item.id + '">' +
                         '<img src="/static/img/agregar-miembro.png" alt="Agregar Integrante" title="Agregar Integrante">' +
                         '</a>' +
                         '<a class="boton-eliminar" href="/configuracion/eliminarSocioResponsable/' + item.id + '">' +
                         '<img src="/static/img/eliminar1.png" alt="Eliminar" title="Eliminar">' +
                         '</a>' +
                         '</div>' +
                         '</td>');

        /* aca abajo retorno la tabla */
        return table.append(user_tmpl);
    };
}