from django.db import models

# Create your models here.

class Sample(models.Model):
    patient_name = models.CharField(max_length=200)
    sample_date = models.DateTimeField(auto_now_add=True)
    sample_Img = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.patient_name