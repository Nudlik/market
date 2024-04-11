from rest_framework import serializers

from ads.models import Ad


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
