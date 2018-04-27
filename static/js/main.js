function Add(num){ 

    num=num+2;;

    var parent = document.getElementsByClassName('list');  

    

    var div = document.createElement('DIV'); 

    div = parent.appendChild(div);  

    div.className="playlist";

    //div.id=num;

    div.innerHTML = 'Playlist#'+num; 

    }  

/*function Del(){

    var parent = document.getElementsByClassName("list");

    var child = document.getElementById(id);

    parent.removeChild(child);

}*/

   

$(document).ready(function() {

    var p = $(".search-wrap");

    var d = $(".playlist-wrap");

    var r = $(".resize");

    var i = $(".input");



          

    var curr_width = p.width()

    var unlock = false;

    

    $(document).mousemove(function(e) {

        var change = curr_width + (e.clientX - curr_width);

        var input_change = curr_width + (e.clientX - curr_width - 100);

        

        if(unlock) {

            

            if(change > 349 && change < 950) {

                p.css("width", change);

                d.css("margin-left", change);

                i.css("width", input_change);

            }     

        }

    });

          

    r.mousedown(function(e) {

        curr_width = p.width();

        unlock = true;

        r.css("background-color", "rgba(1, 1, 1, 1)");

    });

      

    $(document).mousedown(function(e) {

        if(unlock) {

        e.preventDefault();

        }}

    )

    $(document).mouseup(function(e) {

    unlock = false;

    $("#debug").text("");

    r.css("background-color", "rgba(0, 0, 0, 0.1)");

});

    })