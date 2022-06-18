import {getCookie} from "./utilities.js";

let csrftoken;
window.onload = function () {
    $("#nav-registrator").addClass('active');
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
                alert(data.message)
            } else {
                console.log(data);
                $('#keys-div').removeAttr('hidden');
                $('#public-key').text(data.public_key);
                $('#private-key').text(data.private_key);
            }
        }
    });
})