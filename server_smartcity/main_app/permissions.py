from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Kalau cuma minta lihat data (GET), izinkan.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Kalau mau ngedit (PUT) atau hapus (DELETE), 
        # SYARAT 1: Harus pemilik laporannya.
        # SYARAT 2: Status laporan MAKSIMAL cuma boleh DRAFT. 
        # (Kalau udah Verified, otomatis kena blokir 403 Forbidden).
        if request.user == obj.reporter and obj.status == 'DRAFT':
            return True
            
        return False