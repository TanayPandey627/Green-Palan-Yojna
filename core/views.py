from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date

from .models import Mother, Sapling, HealthWorker, PhotoUpload, ReminderLog
from .serializers import (
    MotherSerializer,
    SaplingSerializer,
    HealthWorkerSerializer,
    PhotoUploadSerializer,
    ReminderLogSerializer,
)

# Mother ViewSet
class MotherViewSet(viewsets.ModelViewSet):
    queryset = Mother.objects.all()
    serializer_class = MotherSerializer

# Sapling ViewSet
class SaplingViewSet(viewsets.ModelViewSet):
    queryset = Sapling.objects.all()
    serializer_class = SaplingSerializer

# HealthWorker ViewSet
class HealthWorkerViewSet(viewsets.ModelViewSet):
    queryset = HealthWorker.objects.all()
    serializer_class = HealthWorkerSerializer

# PhotoUpload ViewSet
class PhotoUploadViewSet(viewsets.ModelViewSet):
    queryset = PhotoUpload.objects.all()
    serializer_class = PhotoUploadSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sapling__id', 'uploaded_by__username']

    @action(detail=False, methods=['get'])
    def by_sapling(self, request):
        sapling_id = request.query_params.get('sapling')
        if not sapling_id:
            return Response({"error": "sapling param is required"}, status=400)
        photos = PhotoUpload.objects.filter(sapling_id=sapling_id)
        serializer = self.get_serializer(photos, many=True)
        return Response(serializer.data)

# ReminderLog ViewSet
class ReminderLogViewSet(viewsets.ModelViewSet):
    queryset = ReminderLog.objects.all()
    serializer_class = ReminderLogSerializer

    @action(detail=False, methods=['get'])
    def pending(self, request):
        today = date.today()
        sapling = request.query_params.get('sapling')
        sent_to = request.query_params.get('sent_to')

        reminders = ReminderLog.objects.filter(due_date__lte=today)
        if sapling:
            reminders = reminders.filter(sapling=sapling)
        if sent_to:
            reminders = reminders.filter(sent_to=sent_to)

        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)
