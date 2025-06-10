from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from apps.products.models import Category, Product
from apps.accounts.models import UserProfile
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories...')
        categories = [
            {
                'name': 'Green Tea',
                'slug': 'green-tea',
                'description': 'Fresh and delicate green teas from around the world.',
                'image': 'green-tea.jpg'
            },
            {
                'name': 'Black Tea',
                'slug': 'black-tea',
                'description': 'Rich and robust black teas, perfect for any time of day.',
                'image': 'black-tea.jpg'
            },
            {
                'name': 'Oolong Tea',
                'slug': 'oolong-tea',
                'description': 'Complex and aromatic oolong teas with unique flavors.',
                'image': 'oolong-tea.jpg'
            },
            {
                'name': 'Herbal Tea',
                'slug': 'herbal-tea',
                'description': 'Caffeine-free herbal infusions for relaxation and wellness.',
                'image': 'herbal-tea.jpg'
            }
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                slug=category_data['slug'],
                defaults={
                    'name': category_data['name'],
                    'description': category_data['description']
                }
            )

        self.stdout.write('Creating products...')
        products = [
            {
                'name': 'Dragon Well Green Tea',
                'slug': 'dragon-well-green-tea',
                'description': 'Premium Chinese green tea with a sweet, nutty flavor.',
                'price': 24.99,
                'stock': 100,
                'category': 'green-tea',
                'image': 'dragon-well.jpg'
            },
            {
                'name': 'Earl Grey Black Tea',
                'slug': 'earl-grey-black-tea',
                'description': 'Classic black tea flavored with bergamot oil.',
                'price': 18.99,
                'stock': 150,
                'category': 'black-tea',
                'image': 'earl-grey.jpg'
            },
            {
                'name': 'Tie Guan Yin Oolong',
                'slug': 'tie-guan-yin-oolong',
                'description': 'Premium Chinese oolong tea with a floral aroma.',
                'price': 29.99,
                'stock': 75,
                'category': 'oolong-tea',
                'image': 'tie-guan-yin.jpg'
            },
            {
                'name': 'Chamomile Herbal Tea',
                'slug': 'chamomile-herbal-tea',
                'description': 'Soothing chamomile flowers for relaxation.',
                'price': 14.99,
                'stock': 200,
                'category': 'herbal-tea',
                'image': 'chamomile.jpg'
            }
        ]

        for product_data in products:
            category = Category.objects.get(slug=product_data['category'])
            Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'category': category
                }
            )

        self.stdout.write('Creating superuser...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@teashop.com',
                password='admin123'
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database')) 