from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email: raise ValueError("البريد مطلوب")
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password); user.save(using=self._db); return user
    def create_superuser(self, email, password=None, **extra):
        extra.update(is_staff=True, is_superuser=True, role="admin")
        return self.create_user(email, password, **extra)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=[("admin","مدير"),("editor","محرر"),("moderator","مشرف"),("member","عضو")], default="member")
    preferred_language = models.CharField(max_length=5, default="ar")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self): return self.full_name or self.email
