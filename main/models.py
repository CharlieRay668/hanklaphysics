from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class PhysicsClass(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class Question(models.Model):
    class_choices = (
            (1, "AP Physics"),
            (2, 'Honors Physics'),
            (3, 'Standard Physics'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions", null=True)
    class_link = models.ForeignKey(PhysicsClass, on_delete=models.CASCADE, related_name="classquestions", null=True)
    score = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    physics_class = models.IntegerField(choices=class_choices)
    creation_date = models.DateTimeField()

    def __str__(self):
        return str(self.user) + ' ' + str(self.title)

    def __cmp__(self, other):
        if self.socre > other.score:
            return 1
        if self.score == other.score:
            return 0
        if self.score < other.score:
            return -1
    def __lt__(self, other):
        return self.score < other.score
    def __gt__(self, other):
        return self.score > other.score
    def __le__(self, other):
        return self.score <= other.score
    def __ge__(self, other):
        return self.score >= other.score

class Answer(models.Model):
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", null=True)
    respondee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responses", null=True)
    body = models.TextField()
    score = models.IntegerField()
    creation_date = models.DateTimeField()
    def __cmp__(self, other):
        if self.socre > other.score:
            return 1
        if self.score == other.score:
            return 0
        if self.score < other.score:
            return -1
    def __lt__(self, other):
        return self.score < other.score
    def __gt__(self, other):
        return self.score > other.score
    def __le__(self, other):
        return self.score <= other.score
    def __ge__(self, other):
        return self.score >= other.score



# Create your models here.
