from django.db import models
from django.conf import settings
from django.utils import timezone

# 1. Report Issues
class IssueReport(models.Model):
    CATEGORY_CHOICES = [
        ('TRASH', 'Trash Reporting'),
        ('WATER', 'Water Supply'),
        ('ELECTRICITY', 'Electricity'),
        ('STREETLIGHT', 'Streetlight'),
        ('ROAD', 'Road Maintenance'),
        ('OTHER', 'Other'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    photo = models.ImageField(upload_to='issues/', blank=True, null=True)
    house_no = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.created_at.strftime('%Y-%m-%d')}"

# 2. Emergency Numbers
class EmergencyNumber(models.Model):
    CATEGORY_CHOICES = [
        ('MEDICAL', 'Medical'),
        ('SECURITY', 'Security'),
        ('FIRE', 'Fire Services'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

# 3. Lost & Found
class LostFoundItem(models.Model):
    TYPE_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_found/', blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_lost_found = models.DateField()
    location = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=100, help_text="Phone number or Email")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"

# 4. Local Events & Notices
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 5. Public Feedback / Suggestion
class Feedback(models.Model):
    TYPE_CHOICES = [
        ('FEEDBACK', 'Feedback'),
        ('SUGGESTION', 'Suggestion'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} from {self.user.username}"

# 6. Emergency Alerts
class EmergencyAlert(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 7. Public Chat & Polls
class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text

class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('poll', 'user')

    def __str__(self):
        return f"{self.user.username} voted for {self.option.text}"
