from django.db import models

from profiles.models import Profile


class Misconduct(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    factory = models.CharField(max_length=120, blank=True, null=True)
    position = models.CharField(max_length=120)
    worker_pin = models.IntegerField()
    reason = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='sent_to_hr', choices=(
        ("sent_to_hr", "Kadrga yuborilgan"),
        ("ready_to_sign", "Imzolash uchun tayyor"),
        ("unsigned", "Buyruq hali imzolanmagan"),
        ("signed", "Imzolangan"),
        ("cancelled", "Bekor qilingan"),
    ))
    protocol = models.FileField(upload_to='generated/safety/', null=True, blank=True)
    behest = models.FileField(upload_to='generated/safety/', null=True, blank=True)
    coupon = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname
