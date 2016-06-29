from account.models import Profile

def create_profile(backend, user, response, *args, **kwargs):
    if backend.name == "facebook":
        if user is not None and not hasattr(user, 'profile') and kwargs['is_new']:
            # Get email email
            email = response.get('email')
            if email is not None:
                user.email = email
                user.save()
            # Create user profile
            Profile.objects.create(user=user)
