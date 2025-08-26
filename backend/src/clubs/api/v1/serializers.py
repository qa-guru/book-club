from rest_framework import serializers

from clubs.models import Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ["id", "book_title", "book_authors", "publication_year", "description", "telegram_chat_link", "owner", "members"]
        read_only_fields = ["owner", "members", "created_at", "updated_at", "id"]
