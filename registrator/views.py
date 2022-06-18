from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import rsa
from rsa import VerificationError

from certification_authority.views import is_keys_exchanged

public_key = None
private_key = None


def index(request):
    from voter.views import get_voters_with_public_keys
    voters = User.objects.all()
    voters_public_keys = get_voters_with_public_keys()
    for i in voters_public_keys:
        voters_public_keys[i] = f'e={voters_public_keys[i].e} n={voters_public_keys[i].n}'
    voters_with_public_keys = []
    for i in voters:
        voters_with_public_keys.append({'id': i.id, 'username': i.username, 'public_key': voters_public_keys.get(i.id)})

    return HttpResponse(render(request, 'registrator.html', {'voters': voters_with_public_keys,
                                                             'public_key': None if public_key is None else f'e={public_key.e}\nn={public_key.n}',
                                                             'private_key': None if private_key is None else f'e={private_key.e}\nn={private_key.n}\n'
                                                                                                             f'p={private_key.p}\nq={private_key.q}\nd={private_key.d}'}))


def generate_keys(request):
    global public_key, private_key
    if request.method == 'POST':
        if is_keys_exchanged():
            return JsonResponse({'message': 'Keys have been exchanged'})

        public_key, private_key = rsa.newkeys(512)
        return JsonResponse({'public_key': f'e={public_key.e}\nn={public_key.n}',
                             'private_key': f'e={private_key.e}\nn={private_key.n}\n'
                                            f'p={private_key.p}\nq={private_key.q}\nd={private_key.d}'})


def get_registrator_public_key(request):
    global public_key, private_key
    if request.method == 'GET':
        if public_key is not None:
            return JsonResponse({'public_key': {'e': str(public_key.e), 'n': str(public_key.n)}})
        else:
            return JsonResponse({'message': 'not_ready'})


def get_raw_registrator_public_key():
    global public_key
    return public_key


def sign_voter_ballot(request, voter_id, blind_signed_ballot, signed_blind_signed_ballot):
    from voter.views import get_voter_public_key

    try:
        rsa.verify(str(blind_signed_ballot).encode(),
                   signed_blind_signed_ballot,
                   get_voter_public_key(voter_id))
    except VerificationError:
        return JsonResponse({'message': 'Verify error'})

    return rsa.sign(str(blind_signed_ballot).encode(), private_key, 'SHA-1')
