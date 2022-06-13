from django.db import models

class Record(models.Model):
    name=models.CharField(max_length=100, null=False, unique=True)
    qr_code=models.TextField(null=False)
    hash_id=models.CharField(max_length=500, null=False)
    date_create=models.DateTimeField(auto_now_add=True)
    date_use=models.DateTimeField(null=True, blank=True)
    person_name=models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name