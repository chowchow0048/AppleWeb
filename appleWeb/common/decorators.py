from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def manager_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_manager:
            raise PermissionDenied  # 접근 권한 없음
        return view_func(request, *args, **kwargs)

    return _wrapped_view
