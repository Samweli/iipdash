from django.contrib.auth.forms import UserCreationForm as CoreAdminUserCreationForm

from .models import User


class AdminUserCreationForm(CoreAdminUserCreationForm):

    class Meta:
        model = User
        fields = ("email", "username")
