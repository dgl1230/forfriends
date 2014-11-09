// convert bytes into friendly format
function bytesToSize(bytes) {
        var sizes = ['Bytes', 'KB', 'MB'];
        if (bytes === 0) return 'n/a';
        var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
    }
    // check for selected crop region



function showPreview(coords) {
        var rx = 100 / coords.w;
        var ry = 100 / coords.h;
        $('#small_preview').css({
            width: Math.round(rx * 500) + 'px',
            height: Math.round(ry * 370) + 'px',
            marginLeft: '-' + Math.round(rx * coords.x) + 'px',
            marginTop: '-' + Math.round(ry * coords.y) + 'px'
        }).show();
    }
    // update info by cropping (onChange and onSelect events handler)

function updateInfo(e) {
        x1 = $('#x1').val(e.x);
        y1 = $('#y1').val(e.y);
        x2 = $('#x2').val(e.x2);
        y2 = $('#y2').val(e.y2);
        w = $('#w').val(e.w);
        h = $('#h').val(e.h);

    }

function clearInfo() {
        $('.info #w').val('');
        $('.info #h').val('');
    }
    // Create variables (in this scope) to hold the Jcrop API and image size
var jcrop_api, boundx, boundy;

function fileSelectHandler() {
    // get selected file
    var oFile = $('#image_file')[0].files[0];
    // hide all errors
    $('.error').hide();
    // check for image type (jpg and png are allowed)
    var rFilter = /^(image\/jpeg|image\/png)$/i;
    if (!rFilter.test(oFile.type)) {
        $('.error').html(
            'Please select a valid image file (jpg and png are allowed)'
        ).show();
        return;
    }
    // check for file size
    if (oFile.size > 10000 * 1024) {
        $('.error').html('Please select a smaller image file').show();
        return;
    }
    if (oFile.size < 0) {
        $('.error').html(
            'You have selected too small of a file, please select a larger image file'
        ).show();
        return;
    }
    // preview element
    var oImage = document.getElementById('preview');
    // prepare HTML5 FileReader
    var oReader = new FileReader();
    oReader.onload = function(e) {
        // e.target.result contains the DataURL which we can use as a source of the image
        oImage.src = e.target.result;
        oImage.onload = function() { // onload event handler
            // display step 2
            $('.step2').fadeIn(500);
            // display some basic image info
            var sResultFileSize = bytesToSize(oFile.size);
            $('#filesize').val(sResultFileSize);
            $('#filetype').val(oFile.type);
            $('#filedim').val(oImage.naturalWidth + ' x ' + oImage.naturalHeight);
            // destroy Jcrop if it is existed
            if (typeof jcrop_api != 'undefined') {
                jcrop_api.destroy();
                jcrop_api = null;
                $('#preview').width(oImage.naturalWidth);
                $('#preview').height(oImage.naturalHeight);
            }
           
        };
    };
    // read selected file as DataURL
    oReader.readAsDataURL(oFile);

}