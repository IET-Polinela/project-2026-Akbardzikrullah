from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # === TAMBAHAN BARU: field is_owner ===
    is_owner = serializers.SerializerMethodField()
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)

    class Meta:
        model  = Report
        fields = [
            'id', 'title', 'category', 'description',
            'location', 'status', 'reporter', 'reporter_name',
            'created_at', 'updated_at',
            'is_owner',      # Tambahkan is_owner ke fields
        ]
        read_only_fields = ['reporter', 'is_owner']

    # Method ini otomatis dipanggil saat is_owner di-serialize
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user
        return False