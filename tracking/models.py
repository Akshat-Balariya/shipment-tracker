from django.db import models

# Create your models here.
from django.db import models
import random
import string


def generate_tracking_number():
    return "SHIP-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Shipment(models.Model):
    tracking_number = models.CharField(
        max_length=20, primary_key=True, default=generate_tracking_number, editable=False
    )
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    current_status = models.CharField(max_length=50, default="Created")
    carrier = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tracking_number


class StatusHistory(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=50)
    note = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.shipment.tracking_number} — {self.status}"
