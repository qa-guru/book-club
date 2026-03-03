from rest_framework import serializers
from django.contrib.auth import get_user_model
from clubs.models import Club, BookReview

User = get_user_model()

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ["id", "club", "user", "review", "assessment", "read_pages"]
        read_only_fields = ["created_at", "updated_at", "id"]


class ClubSerializer(serializers.ModelSerializer):
    reviews = BookReviewSerializer(many=True, read_only=True)
    owner = OwnerSerializer(read_only=True)
    
    class Meta:
        model = Club
        fields = ["id", "book_title", "book_authors", "publication_year", "description", "telegram_chat_link", "owner", "members", "reviews"]
        read_only_fields = ["owner", "members", "created_at", "updated_at", "id"]

