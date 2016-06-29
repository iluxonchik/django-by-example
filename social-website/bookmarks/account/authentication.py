from django.contrib.auth.models import User

class EmailAuthBackend(object):
    """
    Authenticate user using an e-mail account
    """
    def authenticate(self, username=None, password=None):
        # We use 'username' and 'password' as kwargs names, so that our backend works with the 
        # authentication framework straight away
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None