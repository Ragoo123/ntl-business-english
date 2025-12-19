from django.db import models
from vocabulary.models import Folder

class ReadingText(models.Model):
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name='reading_texts'
    )
    text_title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text_title

    

class ReadingQuestion(models.Model):
    reading = models.ForeignKey(
        ReadingText,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
    
class ReadingOption(models.Model):
    question = models.ForeignKey(
        ReadingQuestion,
        on_delete=models.CASCADE,
        related_name='options'
    )
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.option_text}"

# Create your models here.
