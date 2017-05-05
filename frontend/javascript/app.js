'use strict';

var Anime = {
    crear_letra_toggle: function($letra) {
        $letra.on('click', function() {
            var $this = $(this);
            if (!$this.hasClass('is-active')) {
                $('li.letra.is-active').toggleClass('is-active');
                $this.toggleClass('is-active');
            } else {
                return;
            }

            var $series = $('.series-letra');
            $series.addClass('is-hidden');

            var $serie_letra = $('#series-letra-' + $this.text().toLowerCase());
            $serie_letra.removeClass('is-hidden');
        });
    },
    crear_letra: function(letra, first) {
        var $letras = $('#letras');
        var $series = $('#series');

        var klass_letras = 'letra';
        var klass_series = 'series-letra is-hidden';

        if (first) {
            klass_letras = 'letra is-active';
            klass_series = 'series-letra';
            first = false;
        }

        var $letra = $("<li class='" + klass_letras + "' id='letra-" + letra + "'><a>" + letra.toUpperCase() + "</a></li>");
        $series.append($("<ul class='" + klass_series + "' id='series-letra-" + letra + "'></ul>"));
        $letras.append($letra);

        this.crear_letra_toggle($letra);
    },
    crear_anime: function(anime, letra) {
        var $card = $("<div class='card'>" +
                        "<div class='card-content'>" +
                          "<p class='title'>" + anime.nombre + "</p>" +
                          "<p>" + anime.descripcion + "</p>" +
                        "</div>" +
                      "</div>");

        var $anime = $('<li></li>');
        $anime.append($card);

        var $series_letra = $('#series-letra-' + letra);
        $series_letra.append($anime);
    },
    crear_animes_por_letra: function(letra, animes) {
        var that = this;
        $.each(animes, function(index, anime) {
            that.crear_anime(anime, letra);
        });
    },
    get_animes: function() {
        var that = this;
        $.get('http://localhost:5000/letra', function(data) {
            var animes = data.animes;

            var first = true;
            $.each(animes, function(letra, animes_por_letra) {
                if ($('#letra-' + letra).length === 0) {
                    that.crear_letra(letra, first);
                }
                first = false;

                that.crear_animes_por_letra(letra, animes_por_letra);
            });
        });
    }
};

Anime.get_animes();
