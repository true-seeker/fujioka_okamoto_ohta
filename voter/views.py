import rsa
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from certification_authority.views import get_public_key, is_keys_exchanged
from registrator.views import get_raw_registrator_public_key

voter_keys = {}
votes = {}


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
                                'public_ca_key': None if public_ca_key is None else f'e={public_ca_key.e}\n'
                                                                                    f'n={public_ca_key.n}',
                                'vote': votes.get(request.user.id)}))


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'voter.html')
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

        public_key, private_key = rsa.newkeys(128)
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
        else:
            votes[request.user.id] = request.POST['candidate_id']
            return JsonResponse({})
