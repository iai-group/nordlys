function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

function show(id) {
	var e = document.getElementById(id);
	e.style.display = "";
}

function hide(id) {
	var e = document.getElementById(id);
	e.style.display = "none";
}


/* Cards */
function show_card(id) {
    var cards = $(".result-card");
    for (i=0; i < cards.length; i++) {
        hide(cards[i].id);
    }
    show(id);
}


function showPop(id, event) {
	var pop_id = "#" + String(id);

    /* 1st, reformat its content. decodeHtml doesn't work, sodecode angle brackets in URI by adding them by script */
    var uri_p = $(pop_id).find("> .el-popup-uri");
    var encoded_html = $(uri_p).html();
//    console.log("P child of " + String(id) + " has this html: " + String(encoded_html) );
    uri_p_text = String($(uri_p).text());
//    console.log("\tP child text: [" + uri_p_text + "]" );
    if (uri_p_text.substring(0,1) !== "<") {
        new_uri_p_text = "<" + uri_p_text + ">";
        $(uri_p).text(new_uri_p_text);
//        console.log("\tReformatting by adding angle brackets to: " + uri_p_text );
    }

    /* Make its width proportional to length of entity name ;) */
	var pop_name_id = "#elPopName" + String(id).substring(5);
	pop_name_text = String($(pop_name_id).text());
	var ideal_pop_width = pop_name_text.length * 8 + (20 * 2); // roughly 8 pxs per char; double padding of 20 (see css)
    var min_pop_width = Math.max(200, ideal_pop_width);  // ideal could be too tiny, so we have a min width of 200
    var final_pop_width = Math.min(800, ideal_pop_width);  // but then could be too much, so we have a max width of 800
//    console.log( "max(" + String(200) + "," + String(ideal_pop_width) + ") = " + String(min_pop_width) +
//     ". Final width to use: " + String(final_pop_width) );
    $(pop_id).css('width', final_pop_width );

    /* OK let's show it */
    var moveLeft = 10;
    var moveDown = 25;
    $(pop_id).css('top', moveDown).css('left', event.pageX - 100);  // substract some left margins+paddings
    $(pop_id).show();  // Important ;P
//    $(pop_id).css('display', "inline-block");
}

function hidePop(id) {
	var pop_id = "#" + String(id);
    $(pop_id).hide();
}


/* ---------------------- Handling request services ---------------------- */
/* Generic to FIX (since it doesn't allow to work the rest parts) and then use it (by passing service arg) */
//function requestService(service, query) {
//    window.location.replace(service + "?query=" + query);
//    console.log("requestService: " service + ".\tQuery: " + query);
//}

/* ER */
function requestERService(query) {
    show("loaderImage");
    console.log("requestERService: " + query);
    window.location.replace("er?query=" + query);  // NOTE: it's NOT "service/er?query="
}

function activateERTab() {
    $("#serviceTabs").children().removeClass("active");
    $("#entityRetrievalTab").addClass("active");
}

function requestERServiceWithCollection(query) {
    var collection = $("#erCollection option:selected").val();
    show("loaderImage");
    console.log("requestERServiceWithIndex: " + collection);
    window.location.replace("er?query=" + query + "&collection=" + collection);
}

/* EL */
function requestELService(query) {
    show("loaderImage");
    console.log("requestELService: " + query);
    window.location.replace("el?query=" + query);  // NOTE: it's NOT "service/el?query="
}

function activateELTab() {
    $("#serviceTabs").children().removeClass("active");
    $("#entityLinkingTab").addClass("active");
}

/* TTI */
function requestTTIService(query) {
    show("loaderImage");
    console.log("requestTTIService: " + query);
    window.location.replace("tti?query=" + query);  // NOTE: it's NOT "service/tti?query="
}

function activateTTITab() {
    $("#serviceTabs").children().removeClass("active");
    $("#ttiTab").addClass("active");
}

function requestTTIServiceWithCollection(query) {
    var collection = $("#ttiCollection option:selected").val();
    show("loaderImage");
    console.log("requestTTIServiceWithIndex: " + collection);
    window.location.replace("tti?query=" + query + "&collection=" + collection);
}

function setSelectedERCollection() {
    var selectedCollectionOption = $("#erCollection option:selected");
    if ( selectedCollectionOption.length ) {
        var collection = selectedCollectionOption.val();
        console.log("requestERServiceWithIndex: " + collection);
        $("#searchBarCollection").val(collection);
    }
    else {
        console.log("Initial query. No erCollection element yet!");
        $("#searchBarCollection").attr("name", "")
    }
}


/* On doc ready */
$(document).ready(function() {
    /* ------------------------- Initializations ------------------------- */
	/* Tabs: Enabling toggable tabs */
	// http://getbootstrap.com/javascript/#tabs
	$('#serviceTabs a').click(function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	})

    // For performance reasons, the Tooltip and Popover data-apis are opt-in, meaning you must initialize them yourself.
    // One way to initialize all tooltips on a page would be to select them by their data-toggle attribute
    // http://getbootstrap.com/javascript/#tooltips
    $(function () {
      $('[data-toggle="tooltip"]').tooltip();
    })

    /* --------------------- Functionalities/Events handling... --------------------- */


    $(function() { /* Decoding EL results */
        console.log("Decoding EL results");

        var results = $("#results .el-result");
        for (i=0; i< results.length; i++){
            var res = results[i];
            var encoded_html = $(res).html();
            $(res).html(decodeHtml(encoded_html));

//            console.log("\tA result: " + String(encoded_html));
//            console.log("\t\tIt should decode into:" + decodeHtml(encoded_html));
        }
    });


});

