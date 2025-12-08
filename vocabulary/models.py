from django.db import models
from django.contrib.auth.models import User

# ---------------------------
# Folder Model
# ---------------------------
class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ---------------------------
# Vocabulary Word Model
# ---------------------------
class VocabularyWord(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=255)
    definition = models.TextField()
    example_sentence = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word

# ---------------------------
# Quiz Score Model
# ---------------------------
class QuizScore(models.Model):
    QUIZ_TYPES = [
        ('vocabulary', 'Vocabulary'),
        ('gapfill', 'Gap Fill'),
        ('listening', 'Listening'),
        ('reading', 'Reading'),
    ]

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='quiz_scores')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_scores')
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPES)
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.folder.name} ({self.quiz_type}): {self.score}"
