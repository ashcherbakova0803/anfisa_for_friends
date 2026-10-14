from django.core.management.base import BaseCommand
from notifications.emails import send_newsletter


class Command(BaseCommand):
    help = 'Отправляет рассылку всем активным подписчикам'

    def add_arguments(self, parser):
        parser.add_argument(
            '--template',
            type=str,
            default='notifications/emails/promo_summer.txt',
            help='Путь к шаблону письма'
        )
        parser.add_argument(
            '--subject',
            type=str,
            default='Новости от «Анфисы для друзей»',
            help='Тема письма'
        )

    def handle(self, *args, **options):
        count = send_newsletter(
            subject=options['subject'],
            template_name=options['template'],
        )
        self.stdout.write(
            self.style.SUCCESS(f'Рассылка отправлена {count} подписчикам.')
        )
