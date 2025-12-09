# users/signals.py
from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up
from django.dispatch import receiver
from django.contrib import messages

@receiver(user_logged_out)
def on_logout(request, user, **kwargs):
    messages.info(request, f"Successfully logged out, {user.username.title()}!")
