import os
import random

import pyaes
import rsa
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rsa import PublicKey

from certification_authority.views import get_public_key, is_keys_exchanged, get_raw_ca_public_key
from registrator.views import get_raw_registrator_public_key, sign_voter_ballot
from utilities import bytes_to_int

voter_keys = {}
votes = {}
secret_keys = {}
encrypted_ballots = {}
blind_signed_ballots = {}
signed_blind_signed_ballots = {}
registrator_signed_ballots = {}
marks = {}


def index(request):
    if not request.user.is_authenticated:
        return redirect('/voter/login')

    if voter_keys.get(request.user.id) is not None:
        public_key = voter_keys[request.user.id][0]
        private_key = voter_keys[request.user.id][1]
    else:
        public_key, private_key = None, None

    if is_keys_exchanged():
        public_ca_key = get_raw_registrator_public_key()
    else:
        public_ca_key = None

    return HttpResponse(render(request, 'voter.html',
                               {'public_key': None if public_key is None else f'e={public_key.e}\n'
                                                                              f'n={public_key.n}',
                                'private_key': None if private_key is None else f'e={private_key.e}\n'
                                                                                f'n={private_key.n}\n'
                                                                                f'p={private_key.p}\n'
                                                                                f'q={private_key.q}\n'
                                                                                f'd={private_key.d}',
                                'secret_key': None if secret_keys.get(request.user.id) is None else list(
                                    secret_keys.get(request.user.id)),
                                'encrypted_ballot': None if encrypted_ballots.get(request.user.id) is None else list(
                                    encrypted_ballots.get(request.user.id)),
                                'blind_signed_ballot': None if blind_signed_ballots.get(
                                    request.user.id) is None else list(
                                    blind_signed_ballots.get(request.user.id)),
                                'signed_blind_signed_ballot': None if signed_blind_signed_ballots.get(
                                    request.user.id) is None else list(
                                    signed_blind_signed_ballots.get(request.user.id)),
                                'registrator_signed_ballot': None if registrator_signed_ballots.get(
                                    request.user.id) is None else list(
                                    registrator_signed_ballots.get(request.user.id)),
                                'mark': None if marks.get(request.user.id) is None else marks.get(request.user.id),
                                'public_ca_key': None if public_ca_key is None else f'e={public_ca_key.e}\n'
                                                                                    f'n={public_ca_key.n}',
                                'vote': votes.get(request.user.id)}))


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/voter')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

    elif request.method == 'GET':
        return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        if len(User.objects.filter(username=request.POST['login'])) != 0:
            return render(request, 'signup.html', {'error': 'user already exists'})

        new_user = User.objects.create_user(username=request.POST['login'], password=request.POST['password'])
        new_user.save()
        login(request, new_user)
        return redirect('/voter')
        # return render(request, 'signup.html')
    elif request.method == 'GET':
        return render(request, 'signup.html')


def generate_keys(request):
    if request.method == 'POST':
        if is_keys_exchanged() and voter_keys.get(request.user.id) is not None:
            return JsonResponse({'message': 'Keys have been exchanged'})

        public_key, private_key = rsa.newkeys(512)
        voter_keys[request.user.id] = (public_key, private_key)
        return JsonResponse({'public_key': f'e={public_key.e}\nn={public_key.n}',
                             'private_key': f'e={private_key.e}\nn={private_key.n}\n'
                                            f'p={private_key.p}\nq={private_key.q}\nd={private_key.d}'})


def get_key_from_ca(request):
    return get_public_key(request)


def get_voters_with_public_keys():
    global voter_keys
    voter_public_keys = {}
    for i in voter_keys:
        voter_public_keys[i] = voter_keys[i][0]
    return voter_public_keys


def vote(request):
    if request.method == 'POST':
        if voter_keys.get(request.user.id) is None:
            return JsonResponse({'message': 'Generate your keys first'})
        if not is_keys_exchanged():
            return JsonResponse({'message': 'Keys have not been exchaned yet'})
        if encrypted_ballots.get(request.user.id) is not None:
            return JsonResponse({'message': 'Ballot already encrypted'})

        votes[request.user.id] = request.POST['candidate_id']
        return JsonResponse({})


def get_secret_key(request):
    if encrypted_ballots.get(request.user.id) is not None:
        return JsonResponse({'message': 'Ballot already encrypted'})

    secret_keys[request.user.id] = os.urandom(16)

    return JsonResponse({'secret_key': str(list(secret_keys[request.user.id]))})


def encrypt_ballot(request):
    if votes.get(request.user.id) is None:
        return JsonResponse({'message': 'Vote first'})
    if secret_keys.get(request.user.id) is None:
        return JsonResponse({'message': 'Generate secret key first'})
    if blind_signed_ballots.get(request.user.id) is not None:
        return JsonResponse({'message': 'Ballot blind signed'})

    aes = pyaes.AESModeOfOperationCTR(secret_keys[request.user.id])
    ciphertext = aes.encrypt(votes[request.user.id])
    encrypted_ballots[request.user.id] = ciphertext

    return JsonResponse({'encrypted_ballot': str(list(ciphertext))})


def blind_sign_ballot(request):
    if votes.get(request.user.id) is None:
        return JsonResponse({'message': 'Vote first'})
    if secret_keys.get(request.user.id) is None:
        return JsonResponse({'message': 'Generate secret key first'})
    if encrypted_ballots.get(request.user.id) is None:
        return JsonResponse({'message': 'Encrypt ballot first'})
    if signed_blind_signed_ballots.get(request.user.id) is not None:
        return JsonResponse({'message': 'Blind signed ballot signed'})
    blind_signed_ballots[request.user.id] = get_raw_ca_public_key().blind(encrypted_ballots[request.user.id][0])

    return JsonResponse({'blind_signed_ballot': str(list(blind_signed_ballots[request.user.id]))})


def sign_blind_signed_ballot(request):
    if votes.get(request.user.id) is None:
        return JsonResponse({'message': 'Vote first'})
    if secret_keys.get(request.user.id) is None:
        return JsonResponse({'message': 'Generate secret key first'})
    if encrypted_ballots.get(request.user.id) is None:
        return JsonResponse({'message': 'Encrypt ballot first'})
    if blind_signed_ballots.get(request.user.id) is None:
        return JsonResponse({'message': 'Blind sign ballot first'})
    if registrator_signed_ballots.get(request.user.id) is not None:
        return JsonResponse({'message': 'Ballot already sent to registrator'})

    signed_blind_signed_ballots[request.user.id] = rsa.sign(
        str(blind_signed_ballots[request.user.id]).encode(), voter_keys[request.user.id][1], 'SHA-1')

    return JsonResponse({'signed_blind_signed_ballot': str(list(signed_blind_signed_ballots[request.user.id]))})


def send_to_registrator(request):
    unblinded = get_raw_ca_public_key().unblind(bytes_to_int(sign_voter_ballot(request,
                                                                               request.user.id,
                                                                               blind_signed_ballots[request.user.id],
                                                                               signed_blind_signed_ballots[
                                                                                   request.user.id])),
                                                blind_signed_ballots[request.user.id][1])

    registrator_signed_ballots[request.user.id] = unblinded
    return JsonResponse({'registrator_signed_ballot': str(registrator_signed_ballots[request.user.id])})


def get_voter_public_key(voter_id) -> PublicKey:
    return voter_keys[voter_id][0]


def generate_mark(request):
    mark = random.randint(2, 2 ** 64)
    marks[request.user.id] = mark
    return JsonResponse({'mark': str(mark)})
