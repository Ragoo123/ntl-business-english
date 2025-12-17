from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from .models import Folder, VocabularyWord, QuizScore, ListeningQuiz, ListeningQuestion, ListeningOption
from .resources import VocabularyResource


@admin.register(ListeningQuestion)
class ListeningQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'listening_quiz', 'question_text')

@admin.register(ListeningOption)
class ListeningOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'option_text', 'is_correct')

@admin.register(ListeningQuiz)
class ListeningQuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'folder', 'audio_file', 'created_at')

@admin.register(VocabularyWord)
class VocabularyAdmin(ImportExportModelAdmin):
    resource_class = VocabularyResource
    list_display = ('word', 'definition', 'folder')
    list_filter = ('folder',)


class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'id')
    exclude = ('owner',)  # hide owner field in form

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = User.objects.get(username='mo')  # Mo is assigned automatically
        super().save_model(request, obj, form, change)

        
admin.site.register(Folder, FolderAdmin)
admin.site.register(QuizScore)
