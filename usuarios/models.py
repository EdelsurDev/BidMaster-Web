from django.contrib.auth.models import AbstractUser
from django.db import models
from licitaciones.models import ProcurementCategory

class Usuario(AbstractUser):
    keywords = models.TextField(blank=True, null=True)
    procurement_categories = models.ManyToManyField(ProcurementCategory, blank=True, related_name='interested_users')

    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

class Permission(models.Model):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')