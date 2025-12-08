from django.contrib import admin
from django.contrib.auth.models import User
from .models import Folder, VocabularyWord, QuizScore

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    exclude = ('owner',)  # hide owner field in form

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = User.objects.get(username='mo')  # Mo is assigned automatically
        super().save_model(request, obj, form, change)

        
admin.site.register(Folder, FolderAdmin)
admin.site.register(VocabularyWord)
admin.site.register(QuizScore)
