from rest_framework import serializers
from common.models import Note
from django.utils.text import slugify

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'name',
            'owner',
            'slug',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = self.context['owner']  
    
    def create(self, validated_data):
        validated_data.pop('files', None)
        validated_data['owner'] = self.owner
        return super().create(validated_data)
    
    def validate_name(self, value):
        slug = slugify('{}-{}'.format(value, self.owner.id))
        reviewer_exists = Note.note.filter(slug=slug).first() is not None

        if reviewer_exists:
            raise serializers.ValidationError("Notes with the same name already exists.")
        return value
