import {getCookie} from "./utilities.js";

let csrftoken;
window.onload = function () {
    $("#nav-ca").addClass('active');

    csrftoken = getCookie('csrftoken');

};

$('#get-keys-from-registrator').on('click', () => {
    $.ajax({
        url: 'exchange_keys',
        type: 'get',
        // data: {
        //     access_token: 'XXXXXXXXXXXXXXXXXXX'
        // },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        // dataType: 'json',
        success: function (data) {
            console.log(data);
            if (data.message !== undefined) {
                alert(data.message)
            } else {
                $('#keys-div').removeAttr('hidden');
                $('#public-ca-key').text(`e=${data.public_ca_key.e} n=${data.public_ca_key.n}`);
            }

        }
    });
})