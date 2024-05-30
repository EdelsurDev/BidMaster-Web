from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Usuario, Role, UserRole

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = Usuario()  # Use the custom user model
        user.username = data.get('preferred_username')
        user.email = data.get('email')
        # Map other fields as needed
        return user

    def save_user(self, request, sociallogin, form=None):
        user = self.populate_user(request, sociallogin, form.cleaned_data if form else {})
        user.save()

        # Assign default role to the user if needed
        default_role = Role.objects.get(name='colaborador')
        UserRole.objects.get_or_create(user=user, role=default_role)

        return user
