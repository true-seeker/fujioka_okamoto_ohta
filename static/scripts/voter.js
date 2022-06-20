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
                console.log(data);
                $('#ca-keys-div').removeAttr('hidden');
                $('#public-ca-key').text(`e=${data.public_ca_key.e} n=${data.public_ca_key.n}`);
            }
        }
    });
})

$('.voter-choice-radio').on('click', (e) => {
    e.preventDefault();
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
                console.log(data);
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
                console.log(data);
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
                console.log(data);
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
                console.log(data);
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
                console.log(data);
                $('#signed-blind-signed-ballot-div').removeAttr('hidden');
                $('#signed-blind-signed-ballot').text(data.signed_blind_signed_ballot);
            }
        }
    });
})

$('#send-to-registrator-button').on('click', () => {
    $.ajax({
        url: 'send_to_registrator',
        type: 'get',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                console.log(data);
                $('#registrator-signed-ballot-div').removeAttr('hidden');
                $('#registrator-signed-ballot').text(data.registrator_signed_ballot);
            }
        }
    });
})

$('#generate-mark-button').on('click', () => {
    $.ajax({
        url: 'generate_mark',
        type: 'get',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                console.log(data);
                $('#generate-mark-div').removeAttr('hidden');
                $('#mark').text(data.mark);
            }
        }
    });
})

$('#send-to-vote-counter-button').on('click', () => {
    $.ajax({
        url: 'send_to_vote_counter',
        type: 'post',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                console.log(data);
                $('#is-sent-to-vote-counter-div').removeAttr('hidden');
            }
        }
    });
})

$('#send-secret-key-to-voter-button').on('click', () => {
    $.ajax({
        url: 'send_secret_key_to_voter',
        type: 'post',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (data) {
            if (data.message !== undefined) {
                alert(data.message);
            } else {
                console.log(data);
                $('#is-secret-key-sent-to-vote-counter-div').removeAttr('hidden');
            }
        }
    });
})
