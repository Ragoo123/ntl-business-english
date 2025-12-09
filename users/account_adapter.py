from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages

class CustomAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):

        # Detect login message template
        if message_template == "account/messages/logged_in.txt":
            user = request.user
            custom_message = f"You are now logged in, {user.get_username().title()}!"
            messages.success(request, custom_message)
            return  # stop allauth from adding its default login message

        # Otherwise use normal Allauth behaviour
        return super().add_message(request, level, message_template, message_context, extra_tags)
