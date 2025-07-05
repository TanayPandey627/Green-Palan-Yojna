from rest_framework import serializers
from .models import Mother, Sapling, HealthWorker, PhotoUpload, ReminderLog


class SaplingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sapling
        fields = '__all__'


class MotherSerializer(serializers.ModelSerializer):
    saplings = SaplingSerializer(many=True, read_only=True)

    class Meta:
        model = Mother
        fields = '__all__'


class HealthWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthWorker
        fields = '__all__'


class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoUpload
        fields = '__all__'


class ReminderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderLog
        fields = '__all__'
