/* Auxiliary functions */

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
function show_card(id, event) {
    var cards = $(".result-card");
    for (i=0; i < cards.length; i++) {
        hide(cards[i].id);
    }

    // Card is shown at same height as doc title;
    var the_card_id = "#" + String(id);
//    $(the_card_id).css('top', event.pageY - 50);  // 200 is about margings
    console.log("event.pageY = " + String(event.pageY));
    $(the_card_id).css('top', "25%");

    show(id);  // Important ;p
}


function showPop(id, event) {
	var pop_id = "#" + String(id);

    /* 1st, reformat its content. decodeHtml doesn't work, so decode angle brackets in URI by adding them by script */
    var uri_p = $(pop_id).find(".el-popup-uri");
    var encoded_html = $(uri_p).html();
    uri_p_text = String($(uri_p).text());
    if (uri_p_text.substring(0,1) !== "<") {
        new_uri_p_text = "<" + uri_p_text + ">";
        $(uri_p).text(new_uri_p_text);
    }

    /* Make its width proportional to length of entity ~~name~~ abstract ;) */
	var pop_inner_elem_id = "#elPopAbstract" + String(id).substring(5);
	pop_inner_elem_text = String($(pop_inner_elem_id).text());
	if (pop_inner_elem_text.length === 0) {  // if abstract is empty, use entity name to redefine dynamic popup width
        var pop_inner_elem_id = "#elPopName" + String(id).substring(5);
        pop_inner_elem_text = String($(pop_inner_elem_id).text());
	}
	// roughly 8 pxs per char; double padding of 20 (see css); 50 is padding-left of popup pic vs popup header
	var ideal_pop_width = pop_inner_elem_text.length * 8 + (20 * 2) + 50;
    var min_pop_width = Math.max(200, ideal_pop_width);  // ideal could be too tiny, so we have a min width of 200
    var final_pop_width = Math.min(400, ideal_pop_width);  // but then could be too much, so we have a max width of 400
//    console.log( "max(" + String(200) + "," + String(ideal_pop_width) + ") = " + String(min_pop_width) +
//     ". Final width to use: " + String(final_pop_width) );
    $(pop_id).css('width', final_pop_width);

    /* Make its height proportional to length of entity abstract ;) */
	var pop_abstract_id = "#elPopAbstract" + String(id).substring(5);
	pop_abstract_text = String($(pop_abstract_id).text());
	var final_pop_height = 100;
	if (pop_abstract_text.length > 0) {  // if abstract is empty, use a fixed height of 100
    	// roughly, for a normal width of 400pxs, it fills ~120pxs with 20 padding_bottom + 100 of content; that content
    	// is span through 6 full rows for an almost full abstract of 400 chars, i.e., ~ 70 chars per row. So we take:
    	// 15px * amounts of rows + padding = 15px * (integer(len / 70) + 1) + 20px
        var ideal_abstract_height = 15 * (Math.floor(pop_abstract_text.length / 70) + 1) + 20;
        // we add it to the min height of 100, not beyond the max of 210
        // 210 is the original set height in styles; ideal for entities with very long abstracts (> 380 chars)
        final_pop_height = Math.min(210, ideal_abstract_height + final_pop_height);
//        console.log("Ideal h = " + String(ideal_abstract_height) + " Final h = " + String(final_pop_height));
	}
    $(pop_id).css('height', final_pop_height);

    /* OK let's show it */
    var moveLeft = 10;
    var moveDown = 25;
    $(pop_id).css('top', moveDown).css('left', event.pageX - 100);  // substract some left margins+paddings
    $(pop_id).show();  // Important ;P
}

function hidePop(id) {
	var pop_id = "#" + String(id);
    $(pop_id).hide();
}


/* ---------------------- Handling request services ---------------------- */

/* ER */
function requestERService(query) {
    show("loaderImage");
    console.log("requestERService: " + query);
    window.location.replace("er?query=" + query);  // NOTE: it's NOT "service/er?query=" even when "service/" was in URL
}

function activateERTab() {
    $("#serviceTabs").children().removeClass("active");
    $("#erTab").addClass("active");
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
    window.location.replace("el?query=" + query);
}

function activateELTab() {
    $("#serviceTabs").children().removeClass("active");
    $("#elTab").addClass("active");
}

/* TTI */
function requestTTIService(query) {
    show("loaderImage");
    console.log("requestTTIService: " + query);
    window.location.replace("tti?query=" + query);
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

function setActionService() {
    var query = $("#searchInputContainer").attr("value");
    // Find current active tab
    var activeTab = $(".active.my-tab");
    if (typeof $(activeTab).html() === 'undefined') {
        $("#searchForm").attr("action", "er?query=" + query);
    }
    else {
        var activeTabId = $(activeTab).attr("id");
        var activeServiceStr = String(activeTabId).split("Tab")[0];
        var actionService = "service_" + activeServiceStr.toUpperCase();

        // Redirect new query to current active tab
        window.location.replace(actionService + "?query=" + query);
    }
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
//        console.log("Decoding EL results");

        var results = $("#results .el-result");
        for (i=0; i< results.length; i++){
            var res = results[i];
            var encoded_html = $(res).html();
            $(res).html(decodeHtml(encoded_html));
        }
    });
});

