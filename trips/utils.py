# Utils that can be used across the whole webapp

def user_is_authenticated(request):
    return request.user.is_authenticated
