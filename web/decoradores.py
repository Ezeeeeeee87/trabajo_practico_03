from django.core.exceptions import PermissionDenied

def role_required(rol):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.rol != rol:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def solo_profesores(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'rol') and request.user.rol == 'profesor':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view