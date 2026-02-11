from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    login_code = ο κωδικός εισόδου που χρησιμοποιεί στο login (μοναδικός).
    Κρατάμε και το default username του Django για συμβατότητα/admin.
    """
    login_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Κωδικός εισόδου (login_code)",
    )

    USERNAME_FIELD = "login_code"
    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return self.login_code
