from rest_framework import serializers
from ..models import Post, Body, Comment
from app.main.api.serializer import CategorySerializer, TagSerializer
from app.account.api.serializer import MyProfileSerializer


class MiniBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ('id', 'body', 'is_script')

class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    author = MyProfileSerializer(read_only=True)
    post_body = MiniBodySerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'image', 'category', 'tags', 'post_body', 'modified_date', 'created_date']


class PostSerializer(serializers.ModelSerializer):
    post_body = MiniBodySerializer(required=False, many=True) # body jonatish kerak majburiy
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'image', 'category', 'tags', 'post_body', 'modified_date', 'created_date')
        extra_kwargs = {
            "author": {"read_only": True},
            "image": {"required": False}
        }

    def create(self, validated_data):
        post_body = validated_data.pop('post_body', None) # tepadan sug'urib olindi, validated_data.pop = bu sug'urib olish
        tags = validated_data.pop('tags', None)
        request = self.context['request']
        user = request.user
        instance = Post.objects.create(author_id=user.id, **validated_data)
        if tags:
            for tag in tags:
                instance.tags.add(tag)
        if post_body:
            for body in post_body: # agar yana qoshimcha body bolsa for aylantiriladi
                Body.objects.create(post_id=instance.id, body=body['body'], is_script=body['is_script'])
        return instance


    def update(self, instance, validated_data):
        post_body = validated_data.pop('post_body', None)
        tags = validated_data.pop('tags', None)
        input_tags = set(tags)
        current_tags = set(instance.tags.all())
        to_remove_tags = current_tags.difference(input_tags)
        to_add_tags = input_tags.difference(current_tags)

        # print(input_tags)
        # print(current_tags)
        # print(to_remove_tags)
        # print(to_add_tags)

        if to_remove_tags:
            for tag in to_remove_tags:
                instance.tags.remove(tag)

        if to_add_tags:
            for tag in to_add_tags:
                instance.tags.add(tag)
        return super(PostSerializer, self).update( instance, validated_data)


class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ('id', 'post', 'body', 'is_script')


class MiniCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "post", "parent_comment", "body", "top_level_comment_id", "created_date")

class CommentSerializer(serializers.ModelSerializer):
    author = MyProfileSerializer(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj): # obj bu commentni otasi
        children = Comment.objects.filter(parent_comment_id=obj.id)
        serializer = MiniCommentSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "parent_comment", "body", "top_level_comment_id", "children", "created_date")
        extra_kwargs = {
            "author": {"read_only": True},
            "top_level_comment_id": {"read_only": True},
            "post": {"read_only": True}
        }

    def create(self, validated_data):
        request = self.context['request']
        post_id = self.context['post_id']
        user_id = request.user.id
        instance = Comment.objects.create(author_id=user_id, post_id=post_id, **validated_data) # **validation - malumotlani dictinary qilib beradi, fields dagi barcha malumotlani beradi
        return instance



# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'author', 'post', 'parent_comment', 'body', 'top_level_comment_id', 'created_date']
