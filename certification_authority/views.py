from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rsa import PublicKey

public_key = None


def index(request):
    global public_key
    return HttpResponse(render(request, 'certification_authority.html',
                               {'public_ca_key': None if public_key is None else f'e={public_key.e}\n'
                                                                                 f'n={public_key.n}', }))


def exchange_keys(request):
    from registrator.views import get_raw_registrator_public_key
    global public_key
    public_key = get_raw_registrator_public_key()
    if public_key is None:
        return JsonResponse({'message': 'Keys have not been generated yet'})
    else:
        return JsonResponse({'public_ca_key': {'e': str(public_key.e), 'n': str(public_key.n)}})


def get_public_key(request):
    global public_key
    if not is_keys_exchanged():
        return JsonResponse({'message': 'Keys have not been exchaned yet'})
    else:
        return JsonResponse({'public_ca_key': {'e': str(public_key.e), 'n': str(public_key.n)}})


def get_raw_ca_public_key() -> PublicKey:
    from registrator.views import get_raw_registrator_public_key
    return get_raw_registrator_public_key()


def is_keys_exchanged():
    global public_key
    if public_key is None:
        return False
    else:
        return True
