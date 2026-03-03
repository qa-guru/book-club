from rest_framework import serializers

from clubs.models import Club, BookReview


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ["id", "club", "user", "review", "assessment", "read_pages"]
        read_only_fields = ["created_at", "updated_at", "id"]


class ClubSerializer(serializers.ModelSerializer):
    reviews = BookReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Club
        fields = ["id", "book_title", "book_authors", "publication_year", "description", "telegram_chat_link", "owner", "members", "reviews"]
        read_only_fields = ["owner", "members", "created_at", "updated_at", "id"]

