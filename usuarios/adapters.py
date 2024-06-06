from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Usuario

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if not user.id:
            try:
                existing_user = Usuario.objects.get(email=user.email)
                sociallogin.connect(request, existing_user)
            except Usuario.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if not user.username:
            user.username = user.email
            user.save()
        return user
