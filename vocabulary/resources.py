from import_export import resources
from .models import VocabularyWord

class VocabularyResource(resources.ModelResource):
    class Meta:
        model = VocabularyWord
        fields = ('id', 'word', 'definition', 'example_sentence', 'folder',)
