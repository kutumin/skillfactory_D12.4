from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Post, Subscriber
from django.template.loader import render_to_string
from django.core.mail import send_mail

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    subscribers = Subscriber.objects.filter()
    html_content = render_to_string('email_template.html', { 'context': instance.article_text, 'article_author':instance.post_author, 'article_id':instance.id})
    for sub in subscribers:
        msg = EmailMultiAlternatives(
            subject='Рассылка по Subscribers',
            body=html_content,
            from_email='skillfacroty@mail.ru',
            to=[sub.email,])
        msg.attach_alternative(html_content, "text/html")
        msg.send()