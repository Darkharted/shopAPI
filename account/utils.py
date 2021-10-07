# account/utils.py
from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    message = f"""
    Congratulation! Вы зарегистрованны на нашем сайте. Пройдите активацию вашего аккаунта 
    отправив нам этот код: {activation_code}
    """
    send_mail(
        'Активация аккаунта',
        message,
        'test@gmail.com',
        [email]
    )