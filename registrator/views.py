from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import rsa

public_key = None
private_key = None


def index(request):
    voters = User.objects.all()
    return HttpResponse(render(request, 'registrator.html', {'voters': voters,
                                                             'public_key': None if public_key is None else f'e={public_key.e}\nn={public_key.n}',
                                                             'private_key': None if private_key is None else f'e={private_key.e}\nn={private_key.n}\n'
                                                                                                             f'p={private_key.p}\nq={private_key.q}\nd={private_key.d}'}))


def generate_keys(request):
    global public_key, private_key
    if request.method == 'POST':
        public_key, private_key = rsa.newkeys(128)
        return JsonResponse({'public_key': f'e={public_key.e}\nn={public_key.n}',
                             'private_key': f'e={private_key.e}\nn={private_key.n}\n'
                                            f'p={private_key.p}\nq={private_key.q}\nd={private_key.d}'})
