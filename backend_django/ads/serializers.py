from rest_framework import serializers

from ads.models import Comment, Ad


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            'pk',
            'image',
            'title',
            'price',
            'description',
        ]


class AdSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField(source='author.phone')
    author_first_name = serializers.SerializerMethodField(source='author.first_name')
    author_last_name = serializers.SerializerMethodField(source='author.last_name')
    author_id = serializers.SerializerMethodField(source='author.id')

    class Meta:
        model = Ad
        fields = [
            'pk',
            'image',
            'title',
            'price',
            'phone',
            'description',
            'author_first_name',
            'author_last_name',
            'author_id',
        ]

    def get_phone(self, obj):
        return obj.author.phone if hasattr(obj, 'author') else None

    def get_author_first_name(self, obj):
        return obj.author.first_name if hasattr(obj, 'author') else None

    def get_author_last_name(self, obj):
        return obj.author.last_name if hasattr(obj, 'author') else None

    def get_author_id(self, obj):
        return obj.author.id if hasattr(obj, 'author') else None

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        ad = self.Meta.model.objects.create(**validated_data)
        ad.save()
        return ad


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField(source='author.first_name')
    author_last_name = serializers.SerializerMethodField(source='author.last_name')
    ad_id = serializers.SerializerMethodField(source='ad.id')
    author_image = serializers.SerializerMethodField(source='author.image')

    class Meta:
        model = Comment
        fields = [
            'pk',
            'text',
            'author_id',
            'created_at',
            'author_first_name',
            'author_last_name',
            'ad_id',
            'author_image',
        ]

    def get_author_first_name(self, obj):
        return obj.author.first_name if hasattr(obj, 'author') else None

    def get_author_last_name(self, obj):
        return obj.author.last_name if hasattr(obj, 'author') else None

    def get_ad_id(self, obj):
        return obj.ad.id if hasattr(obj, 'ad') else None

    def get_author_image(self, obj):
        try:
            return obj.author.image.url
        except (AttributeError, ValueError):
            return None

    def save(self, **kwargs):
        self.validated_data['author'] = self.context['request'].user
        self.validated_data['ad_id'] = self.context['request'].stream.resolver_match.kwargs['ad_pk']

        if pk := self.data.get('pk'):
            self.validated_data['pk'] = pk
        comment, created = self.Meta.model.objects.update_or_create(pk=pk, defaults=self.validated_data)
        if not created:
            comment.save()

        self.instance = comment
        return comment
