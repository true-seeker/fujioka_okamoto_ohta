import {getCookie} from "./utilities.js";

let csrftoken;
window.onload = function () {
    $("#nav-voter").addClass('active');
    csrftoken = getCookie('csrftoken');

};
$('#generate-keys-button').on('click', () => {
    $.ajax({
        url: 'generate_keys',
        type: 'post',
        // data: {
        //     access_token: 'XXXXXXXXXXXXXXXXXXX'
        // },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        // dataType: 'json',
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                console.log(data);
                $('#keys-div').removeAttr('hidden');
                $('#public-key').text(data.public_key);
                $('#private-key').text(data.private_key);
            }
        }
    });
})

$('#get-keys-from-ca-button').on('click', () => {
    $.ajax({
        url: 'get_key_from_ca',
        type: 'get',
        // data: {
        //     access_token: 'XXXXXXXXXXXXXXXXXXX'
        // },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        // dataType: 'json',
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                $('#ca-keys-div').removeAttr('hidden');
                $('#public-ca-key').text(`e=${data.public_ca_key.e} n=${data.public_ca_key.n}`);
            }
        }
    });
})