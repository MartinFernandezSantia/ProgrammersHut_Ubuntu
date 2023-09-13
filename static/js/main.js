var mediaQuery = window.matchMedia('(max-width: 1023px)');
let dropdown = $("#avatar_dropdown")
mediaQuery.addEventListener('change', function(mq){
	if (!mq.matches) {
		dropdown.addClass("dropstart");
		dropdown.removeClass("dropend");
	} else {
		dropdown.addClass("dropend");
		dropdown.removeClass("dropstart");
	}
})

$("#search").autocomplete({
    source: "/buscar_usuario/",
    minLength: 2,
}).data("uiAutocomplete")._renderItem = function (ul, item) {
    return $("<li />")
        .data("item.autocomplete", item)
        .append("<div class='p-2'><a href='' class='nav-link'><img src='" + item.avatar + "' width='30'/>" + item.label + "</a></div>")
        .appendTo(ul);
};