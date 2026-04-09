from rest_framework import permissions

class RolAsosidaRuxsat(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.roli == 'ADMIN':
            return True
        
        ruxsat_etilgan = {
            'OQITUVCHI': [
                'student_list', 'student_create', 'student_edit',
                'attendance_list', 'attendance_create', 'attendance_bulk'
            ],
            'OTA_ONA': [
                'parent_dashboard', 'child_details', 'child_attendance'
            ]
        }
        
        view_name = getattr(view, 'permission_name', view.__class__.__name__)
        
        if request.user.roli in ruxsat_etilgan:
            return view_name in ruxsat_etilgan[request.user.roli]
        
        return False


class AdminRuxsati(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roli == 'ADMIN'


class OqituvchiRuxsati(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roli == 'OQITUVCHI'


class OtaOnaRuxsati(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roli == 'OTA_ONA'