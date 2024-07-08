from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class Container(models.Model):
  
  dummy_user = User.objects.all().filter(id=8).first()
  
  name = models.CharField(max_length=20)
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=dummy_user.pk)
  
  def get_entries(self):
    entries = Entry.objects.filter(container=self.id)
    return entries
  
  class Meta:
    verbose_name = "container"
    verbose_name_plural = "containers"

  def __str__(self):
    return self.name+', '+self.user.username

class Entry(models.Model):
    
  title = models.CharField(max_length=30, null=False)
  body = models.TextField(max_length=5000, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  container = models.ForeignKey(Container, on_delete=models.CASCADE)
  
  class Meta:
    verbose_name = "entry"
    verbose_name_plural = "entries"

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("_detail", kwargs={"pk": self.pk})




  


