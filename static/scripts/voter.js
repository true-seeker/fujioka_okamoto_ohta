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
        headers: {
            'X-CSRFToken': csrftoken,
        },
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
        headers: {
            'X-CSRFToken': csrftoken,
        },
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

$('.voter-choice-radio').on('click', (e) => {
    e.preventDefault();
    console.log(e.target);
    console.log(e.target.dataset.candidateId);
    $.ajax({
        url: 'vote',
        type: 'post',
        data: {
            candidate_id: e.target.dataset.candidateId
        },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                $('.voter-choice-radio').prop('checked', false);
                $(e.target).prop('checked', true);
            }
        }
    });
})

$('#get-secret-key').on('click', () => {
    $.ajax({
        url: 'get_secret_key',
        type: 'get',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                $('#secret-key-div').removeAttr('hidden');
                $('#secret-key').text(data.secret_key);
            }
        }
    });
})


$('#encrypt-ballot-button').on('click', () => {
    $.ajax({
        url: 'encrypt_ballot',
        type: 'get',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                $('#encrypted-ballot-div').removeAttr('hidden');
                $('#encrypted-ballot').text(data.encrypted_ballot);
            }
        }
    });
})

$('#blind-sign-button').on('click', () => {
    $.ajax({
        url: 'blind_sign_ballot',
        type: 'get',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                $('#blind-signed-ballot-div').removeAttr('hidden');
                $('#blind-signed-ballot').text(data.blind_signed_ballot);
            }
        }
    });
})

$('#sign-blind-sign-button').on('click', () => {
    $.ajax({
        url: 'sign_blind_signed_ballot',
        type: 'get',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                $('#signed-blind-signed-ballot-div').removeAttr('hidden');
                $('#signed-blind-signed-ballot').text(data.signed_blind_signed_ballot);
            }
        }
    });
})
