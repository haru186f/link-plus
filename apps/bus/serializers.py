from rest_framework import serializers
from .models import BusStop, BusSchedule


class BusStopSerializer(serializers.ModelSerializer):
    """バス停シリアライザー"""
    class Meta:
        model = BusStop
        fields = ['id', 'name']
