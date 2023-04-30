from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.licenciamiento.choices import CHOICE_PROVINCIA


class Cargo(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False)

    class Meta:
        db_table = 'Cargo'
        verbose_name = 'Cargos'
        verbose_name_plural = 'Cargo'

    def __str__(self):
        return f'Cargo: {self.nombre}.'

class Usuario(AbstractUser):
    fk_cargo = models.ForeignKey(Cargo, verbose_name='Cargo', blank=True, null=True, on_delete=models.CASCADE)
    provincia = models.CharField(verbose_name='Provincia que atiende', max_length=50, choices=CHOICE_PROVINCIA, blank=True,
                                 null=True)

    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        else:
            query = Usuario.objects.get(pk=self.pk)
            if query.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)