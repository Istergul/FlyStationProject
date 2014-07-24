/**
 * Created by Istergul on 23.07.14.
 */

function getRandomInRange(from, to, fixed) {
    return (Math.random() * (to - from) + from).toFixed(fixed) * 1;
}

$(document).ready(function() {

    $('#randomBtn').on("click", function(e) {
        var rndLtd = getRandomInRange(-90, 90, 2),
            rndLng = getRandomInRange(-180, 180, 2);

        $('#pointForm input').parent().removeClass('has-error');
        $('#id_latitude').val(rndLtd);
        $('#id_longitude').val(rndLng);
        $('#checkError').hide();
        $('#checkSuccess').hide();
    });

    var checkRequestLock = false;

    $('#pointForm').on("submit", function(e){
        e.preventDefault();
        $(this).find('input').parent().removeClass('has-error');

        if (!checkRequestLock) {
            checkRequestLock = true;
            var obj = {
                latitude: $(this).find('#id_latitude').val(),
                longitude: $(this).find('#id_longitude').val()
            };
            $.ajax({url: "/check-point/", type: "GET", data: obj})
            .done(function(data) {
                if (data.result) {
                    $('#checkSuccess').show();
                    $('#checkError').hide();
                } else {
                    $('#checkSuccess').hide();
                    $('#checkError').show();
                }
            }).fail(function(xhr) {
                var k;
                for (k in xhr.responseJSON) if (xhr.responseJSON.hasOwnProperty(k)) {
                    $('#pointForm input[name='+k+']').parent().addClass('has-error');
                }
            }).always(function() {
                checkRequestLock = false;
            });
        }

        return false;
    });

});