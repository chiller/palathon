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
    $("#results").css(
        "background-color",
        getColorString(colorThief.getColor(image))
    );

    colorThief.getPalette(image).forEach(function(color){
       var colorstring = getColorString(color)
       paletteelem =  "<div class='paletteresult' style='background-color:" + colorstring +" ' ></div>" ;
       $("#palette").append(paletteelem);
    })


}

$(function(){
    initDropZone()
    colorThief = new ColorThief();
})
