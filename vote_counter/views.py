from django.http import HttpResponse
from django.shortcuts import render
import pyaes

from registrator.views import get_raw_registrator_public_key

encrypted_votes = []
decrypted_votes = []


def index(request):
    return HttpResponse(render(request, 'vote_counter.html', {'encrypted_votes': encrypted_votes,
                                                              'decrypted_votes': decrypted_votes}))


def accept_vote_from_voter(mark, encrypted_ballot, hidden_encrypted_ballot):
    voter_public_key = get_raw_registrator_public_key()
    # is_ok = rsa.verify(encrypted_ballot, hidden_encrypted_ballot, voter_public_key)
    # if not is_ok:
    #     return False
    for index, elem in enumerate(encrypted_votes):
        if elem['mark'] == mark:
            encrypted_votes[index] = {'mark': mark,
                                      'encrypted_ballot': encrypted_ballot,
                                      'hidden_encrypted_ballot': list(hidden_encrypted_ballot)}
            break
    else:
        encrypted_votes.append({'mark': mark,
                                'encrypted_ballot': encrypted_ballot,
                                'hidden_encrypted_ballot': list(hidden_encrypted_ballot)})

    return True


def accept_secret_key_from_voter(mark, secret_key):
    for index, elem in enumerate(encrypted_votes):
        if elem['mark'] == mark:
            encrypted_ballot = elem['encrypted_ballot']
            break
    aes = pyaes.AESModeOfOperationCTR(secret_key)
    decrypted_ballot = aes.decrypt(encrypted_ballot)

    for index, elem in enumerate(decrypted_votes):
        if elem['mark'] == mark:
            decrypted_votes[index] = {'mark': mark,
                                      'secret_key': secret_key,
                                      'ballot': str(decrypted_ballot)}
            break
    else:
        decrypted_votes.append({'mark': mark,
                                'secret_key': list(secret_key),
                                'ballot': decrypted_ballot.decode('utf-8')})

    return True
