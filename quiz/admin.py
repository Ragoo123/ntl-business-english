from django.contrib import admin
from .models import ReadingText, ReadingQuestion, ReadingOption


@admin.register(ReadingText)
class ReadingTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_title', 'folder', 'created_at')
    search_fields = ('text',)


@admin.register(ReadingQuestion)
class ReadingQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'reading', 'question_text')
    search_fields = ('question_text',)


@admin.register(ReadingOption)
class ReadingOptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_reading_title',
        'question',
        'option_text',
        'is_correct',
    )
    list_filter = ('is_correct',)

    def get_reading_title(self, obj):
        return obj.question.reading.text_title

    get_reading_title.short_description = "Reading Title"