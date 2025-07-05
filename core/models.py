from django.db import models
from django.utils import timezone
from datetime import timedelta

class Mother(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    delivery_date = models.DateField()
    health_center = models.CharField(max_length=255)
    address = models.TextField()
    geolocation = models.CharField(max_length=255)
    pledge_signed = models.BooleanField(default=False)
    pledge_photo = models.ImageField(upload_to='pledges/', null=True, blank=True)

    def __str__(self):
        return self.name


class HealthWorker(models.Model):
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Sapling(models.Model):
    PLANT_TYPES = [
        ('Mango', 'Mango'),
        ('Guava', 'Guava'),
        ('Indian Gooseberry', 'Indian Gooseberry'),
        ('Papaya', 'Papaya'),
        ('Drumstick', 'Drumstick'),
    ]
    mother = models.ForeignKey(Mother, on_delete=models.CASCADE, related_name='saplings')
    plant_type = models.CharField(max_length=50, choices=PLANT_TYPES)
    planted_date = models.DateField()
    geolocation = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.plant_type} for {self.mother.name}"


class PhotoUpload(models.Model):
    sapling = models.ForeignKey(Sapling, on_delete=models.CASCADE, related_name='photos')
    uploaded_by = models.ForeignKey(HealthWorker, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='sapling_photos/')
    upload_date = models.DateField(auto_now_add=True)
    week_number = models.PositiveIntegerField(null=True, blank=True)
    geotag_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            reminder_type = "Weekly" if self.week_number and self.week_number <= 4 else "Fortnightly"
            days_until_next = 7 if reminder_type == "Weekly" else 15
            due = self.upload_date + timedelta(days=days_until_next)

            ReminderLog.objects.create(
                sapling=self.sapling,
                reminder_type=reminder_type,
                due_date=due,
                message=f"Next photo is due in {days_until_next} days for sapling: {self.sapling}",
                sent_to=self.uploaded_by.username if self.uploaded_by else "Unknown"
            )


class ReminderLog(models.Model):
    sapling = models.ForeignKey(Sapling, on_delete=models.CASCADE, related_name='reminders')
    reminder_date = models.DateField(auto_now_add=True)
    reminder_type = models.CharField(max_length=100)  # 'Weekly' or 'Fortnightly'
    due_date = models.DateField()
    message = models.TextField()
    sent_to = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sapling} - {self.reminder_type} due {self.due_date}"
