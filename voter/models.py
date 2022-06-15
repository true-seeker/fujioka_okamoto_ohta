from django.db import models


# Create your models here.
class Voter(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    public_key = models.JSONField(verbose_name='public key')
    private_key = models.JSONField(verbose_name='private key')
    secret_key = models.JSONField(verbose_name='secret key')
