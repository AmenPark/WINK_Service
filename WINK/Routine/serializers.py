from rest_framework import serializers
from .models import routine, routine_day, routine_result

class routineSerializer(serializers.ModelSerializer):
    class Meta:
        model = routine
        fields = '__all__'

class routine_daySerializer(serializers.ModelSerializer):
    class Meta:
        model = routine_day
        fields = '__all__'

class routine_resultSerializer(serializers.ModelSerializer):
    class Meta:
        model = routine_result
        fields = '__all__'