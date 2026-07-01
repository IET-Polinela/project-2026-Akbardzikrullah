from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # === TAMBAHAN BARU: field is_owner dan reporter name dengan privacy ===
    is_owner = serializers.SerializerMethodField()
    reporter = serializers.SerializerMethodField()  # Override to return 'Warga Anonim'
    reporter_name = serializers.SerializerMethodField()  # Changed to SerializerMethodField for privacy

    class Meta:
        model  = Report
        fields = [
            'id', 'title', 'category', 'description',
            'location', 'status', 'reporter', 'reporter_name',
            'created_at', 'updated_at',
            'is_owner',      # Tambahkan is_owner ke fields
        ]
        read_only_fields = ['reporter', 'is_owner']

    # Method untuk field reporter: SELALU return 'Warga Anonim' untuk privasi
    def get_reporter(self, obj):
        return 'Warga Anonim'
    
    # Method ini otomatis dipanggil saat is_owner di-serialize
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user
        return False
    
    # Privacy-aware reporter_name: show actual name to owner, anonymize for others
    def get_reporter_name(self, obj):
        request = self.context.get('request')
        
        # Jika context kosong atau tidak ada request, return 'Warga Anonim'
        if not request:
            return 'Warga Anonim'
        
        # Jika user terautentikasi dan adalah pemilik laporan, tampilkan username asli
        if request.user and request.user.is_authenticated and obj.reporter == request.user:
            return obj.reporter.username
        
        # Untuk selain itu (non-owner), return 'Warga Anonim'
        return 'Warga Anonim'