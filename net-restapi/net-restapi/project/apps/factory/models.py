from django.db import models
from django.core.validators import MinValueValidator


class Equipment(models.Model):
    code_equip = models.UUIDField(unique=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False)
    representation_unit = models.CharField(max_length=128)
    representation_code = models.CharField(max_length=200)
    representation_period = models.IntegerField(validators=[MinValueValidator(1)], help_text='number of months')
    expire = models.DateTimeField(null=False)
    state_code = models.UUIDField(unique=True)
    name = models.CharField(max_length=128, null=False, blank=False)
    equipment_model = models.CharField(max_length=128)
    country = models.CharField(max_length=32)
    image = models.FileField(upload_to='docs')


class Emergency(models.Model):
    state_code = models.ForeignKey(to=Equipment, to_field='state_code', on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False)
    reason_operator = models.TextField()
    reason_repairman = models.TextField(null=True)
    repair_date = models.DateTimeField(null=True)
    repair_code = models.UUIDField(unique=True, null=False, blank=False)
