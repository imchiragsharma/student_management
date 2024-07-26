from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
    parent_name = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.parent_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
    student_name = models.CharField(max_length=100)
    student_phone_number = models.CharField(max_length=15, unique=True)
    class_name = models.CharField(max_length=50)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')
    class_teacher_name = models.CharField(max_length=100)
    chemistry = models.FloatField(null=True, blank=True)
    physics = models.FloatField(null=True, blank=True)
    math = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.student_name

@receiver(post_save, sender=Student)
def create_student_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.student_phone_number, password=instance.student_phone_number)
        instance.user = user
        instance.save()

@receiver(post_save, sender=Parent)
def create_parent_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.parent_phone_number, password=instance.parent_phone_number)
        instance.user = user
        instance.save()
