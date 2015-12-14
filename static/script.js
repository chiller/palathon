function initDropZone(){
    var dropZone = document.getElementById('dropZone');

    // Optional.   Show the copy icon when dragging over.  Seems to only work for chrome.
    dropZone.addEventListener('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
    });

    // Get file data on drop
    dropZone.addEventListener('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
        var files = e.dataTransfer.files; // Array of all files
        for (var i=0, file; file=files[i]; i++) {
            if (file.type.match(/image.*/)) {
                var reader = new FileReader();
                reader.onload = function(e2) { // finished reading file data.
                    var img = document.createElement('img');
                    img.height = 100;
                    img.src= e2.target.result;
                    document.getElementById("dropZone").appendChild(img);

                    // Must wait for image to load in DOM, not just load from FileReader
                    image = $("#dropZone img")[0]
                    $(image).on('load', function() {
                      showColorsForImage(image);
                    });
                }
                reader.readAsDataURL(file); // start reading the file data.
    }   }   });
}

function showColorsForImage(image){

    var getColorString = function(color) {
        colorstring = color.join(", ")
        return "rgba(" + colorstring + ",100)";
    }
    var main_color = colorThief.getColor(image);
    $("#maincolor").css(
        "background-color",
        getColorString(main_color)
    );

    colorThief.getPalette(image).forEach(function(color){
       var colorstring = getColorString(color)
       paletteelem =  "<div class='paletteresult' style='background-color:" + colorstring +" ' ></div>" ;
       $("#palette").append(paletteelem);
    })

    getResultsForImage(main_color);
}

function getResultsForImage(color){

    $.get("/colors/5/"+ color.join("/"), function(result){
        result.forEach(function(elem, i){
        $("#results").append("<a href='"+elem.product_url+"'><img src='"+ elem.gallery_img +"' </img></a>")
    })
})}

$(function(){
    initDropZone()
    colorThief = new ColorThief();
})
