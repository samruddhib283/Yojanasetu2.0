from django.db import models
from django.contrib.auth.models import User

class SchemeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    income = models.IntegerField()
    occupation = models.CharField(max_length=100)
    schemes_suggested = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.occupation} - {self.submitted_at.strftime('%Y-%m-%d')}"

class Scheme(models.Model):
    name = models.CharField(max_length=255)
    ministry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    launch_year = models.CharField(max_length=10)
    cs_css = models.CharField(max_length=10)
    summary = models.TextField()
    wiki_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

# models.py
class SchemeHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    occupation = models.CharField(max_length=100)
    income = models.IntegerField()
    category = models.CharField(max_length=50, default="General")
    
    recommended_schemes = models.TextField()  # Store full response here
