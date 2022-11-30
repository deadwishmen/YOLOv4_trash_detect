$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#img').hide();
    $('.recycle-bin').hide();
    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            $('#img').hide();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        var upBtn = document.getElementById("upload-file");
        upBtn.getElementsByClassName("upload-label")[0].style.margin = "0";
        $('.recycle-bin').hide();
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        readURL(this);
        var Bin = document.getElementById("uinf");
        Bin.getElementsByClassName("recycle-bin")[0].style.position = "relative";
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.recycle-bin').show();
                $('.loader').hide();
                $('#img').attr('src', '../static/img/' + data);
                $('#img').show();
                $('#result').text(' Model predicts the garbage as:  ' + data);
                console.log(data)
                console.log('Success!');
            },
        });
    });

});
