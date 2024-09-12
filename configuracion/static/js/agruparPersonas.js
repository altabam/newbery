function __init() {
    $('#search_input')/* inicializamos el buscador */
        .val('')
        .focus()
        .keyup(function() {
            if (!$.trim($(this).val())) {
                $('#listPersonas .error').empty().hide();
            }
        });

    var cache = {};
    $('#search_input').autocomplete({ /* configuracion de autocompletado incluso sin tener min */
        minLength: 0,
        select: function(event, ui) {
            return false;  // Previene que se seleccione automáticamente
        },
        open: function() {
            $('#listPersonas').html($(this).autocomplete("widget").html());
            $(this).autocomplete("widget").hide();
        },
        source: function(request, response) {/* Busca el termino de busqueda en cache */
            if (cache[request.term]) {
                console.log("request.term"+cache[request.term]);
                response(cache[request.term]);
                return;
            }

            $.ajax({ /* Si no está en cache, hace una peticion con ajax */
                dataType: 'json',
                method: 'GET',
                url: '/configuracion/buscarPersona/',
                data: {  /* le envia el termino de busqueda con un codigo por seguridad */
                    q: encodeURIComponent(request.term),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(data) {
                    console.log(data);
                    var personas = [];
                    console.log(data);
                    for (var x in data) {
                        console.log(data[x].fields.numero);
                        personas.push({
                            indice: x,
                            id: data[x].pk,
                            dni: data[x].fields.dni,
                           /*  numero: data[x].fields.numero, */
                            nombre: data[x].fields.nombre,
                            apellido: data[x].fields.apellido,
                            fecha_nacimiento: data[x].fields.fecha_nacimiento,
                            telefono: data[x].fields.telefono,
                            direccion: data[x].fields.direccion,
                        });
                    }
                    
                   
                    cache[request.term] = personas;
                    response(personas);
                }
            });
        },
        response: function(event, ui) {
            if (!ui.content.length) {
                $('#listPersonas').empty();
            } else {
            }
        }
    }).autocomplete('instance')._renderItem = function(table, item) {
        console.log("item:" + item.apellido);
        var user_tmpl = $('<tr />')
                        .addClass('tr');

        user_tmpl.append('<td>' + item.indice + '</td>');
        user_tmpl.append('<td class="tdNumero">' + item.id + '</td>');
        user_tmpl.append('<td class="tdNumero">' + item.dni + '</td>');
        user_tmpl.append('<td class="td-nombre">' + item.nombre + '</td>');
        user_tmpl.append('<td class="td-nombre">' + item.apellido + '</td>');
        user_tmpl.append('<td class="td-numero">' + item.fecha_nacimiento + '</td>');
        user_tmpl.append('<td class="td-numero">' + item.telefono + '</td>');
        user_tmpl.append('<td class="td-nombre">' + item.direccion + '</td>');
        user_tmpl.append('<td class="td-opciones" colspan="3">' +
                         '<div class="divBoton">' +
                         '<a class="boton-editar" href="' + item.id + '">' +
                         '<img src="/static/img/agregar-miembro.png" alt="Agregar Integrante" title="Agregar Integrante">' +
                         '</a>' +
                         '<a class="boton-eliminar" href="' + item.id + '">' +
                         '<img src="/static/img/eliminar1.png" alt="Eliminar" title="Eliminar">' +
                         '</a>' +
                         '</div>' +
                         '</td>');

        /* aca abajo retorno la tabla */
        return table.append(user_tmpl);
    };
}