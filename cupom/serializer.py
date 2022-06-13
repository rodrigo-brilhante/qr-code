from rest_framework import serializers
from cupom.models import Record

class CupomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record 
        fields = '__all__'


