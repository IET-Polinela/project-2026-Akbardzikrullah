from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 
            'created_at', 'updated_at'
        ]

    # Fungsi ini akan otomatis dipanggil oleh field 'reporter' di atas
    def get_reporter(self, obj):
        # Setiap kali API dipanggil, nama pelapor akan selalu muncul sebagai teks ini
        return "Warga Anonim"