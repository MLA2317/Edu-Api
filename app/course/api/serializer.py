from rest_framework import serializers
from ..models import Course, Lesson, LessonFiles, SoldCourse
from app.main.api.serializer import CategorySerializer, TagSerializer


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Course
        fields = ['id', 'author', 'title', 'category', 'cover', 'difficulty', 'get_difficulty_display', 'body', 'price', 'discount_price',
                  'is_free', 'tags']
        extra_kwargs = {
            'author': {'read_only': True},
            'cover': {'required': False}
        }

    def create(self, validated_data):
        category = validated_data.pop('category')
        tags = validated_data.pop('tags')
        request = self.context['request']
        user_id = request.user.id
        instance = super().create(**validated_data)
        instance.author_id = user_id
        instance.category = category.get('id')
        if tags:
            for tag in tags:
                instance.tags.add(tag.get('id'))
        instance.save()
        return instance

