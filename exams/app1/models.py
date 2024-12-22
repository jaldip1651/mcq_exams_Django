from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Exam(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=150)

    def __str__(self):
        return self.text


class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    answers = models.JSONField()
    score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"
