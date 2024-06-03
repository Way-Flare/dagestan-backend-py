from user.models import User


class UserService:

    @staticmethod
    def email_already_exists(email: str):
        email_exists = User.objects.filter(email=email).exists()
        return email_exists
