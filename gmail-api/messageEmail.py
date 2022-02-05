import base64
from email.message import Message
from email.mime.text import MIMEText


def create_message(sender, to, subject, message_text):
    """Create a message for an email

    sender -> Email address of the sender.
    to => Email address of the receiver.
    message_text: The text of the email message
    """

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_sting())}

def send_message(service, user_id, message):
    """Send an email message
    
    Args:
        service: gmail api service instance
        user_id: User's email address. {see special value "me"}
        message: Message to be sent
        Returns: Sent Message
    """
    pass

    