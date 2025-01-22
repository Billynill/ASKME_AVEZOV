from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Post, Answer, Tag, Rating, Author, Profile
from faker import Faker
import random
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения сущностей')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        users = []
        for _ in range(ratio):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password',
                email=fake.email(),
            )
            Profile.objects.create(user=user, avatar=None)
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'{len(users)} пользователей добавлено'))

        authors = []
        for _ in range(ratio):
            author = Author.objects.create(name=fake.name())
            authors.append(author)
        self.stdout.write(self.style.SUCCESS(f'{len(authors)} авторов добавлено'))

        tags = []
        for _ in range(ratio):
            tag = Tag.objects.create(name=fake.word())
            tags.append(tag)
        self.stdout.write(self.style.SUCCESS(f'{len(tags)} тегов добавлено'))

        def generate_image():
            image = Image.new('RGB', (100, 100), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            buffer.seek(0)
            return ContentFile(buffer.read(), 'image.jpg')

        posts = []
        for _ in range(ratio * 10):
            post = Post.objects.create(
                title=fake.sentence(),
                author=random.choice(authors),
                content=fake.text(),
                likes=random.randint(0, 100),
                image=generate_image(),
            )
            post.tags.set(random.sample(tags, k=random.randint(1, len(tags))))
            posts.append(post)
        self.stdout.write(self.style.SUCCESS(f'{len(posts)} постов добавлено'))

        answers = []
        for _ in range(ratio * 100):
            answer = Answer.objects.create(
                text=fake.text(),
                author=random.choice(authors),
                post=random.choice(posts),
                is_accepted=random.choice([True, False]),
            )
            answers.append(answer)
        self.stdout.write(self.style.SUCCESS(f'{len(answers)} ответов добавлено'))

        ratings = []
        for _ in range(ratio * 200):
            author = random.choice(authors)
            post = random.choice(posts)
            value = random.randint(1, 5)

            if not Rating.objects.filter(author=author, post=post).exists():
                rating = Rating.objects.create(
                    author=author,
                    post=post,
                    value=value,
                )
                ratings.append(rating)
            else:
                self.stdout.write(self.style.WARNING(f'Rating уже существует для author={author} и post={post}'))


        self.stdout.write(self.style.SUCCESS(f'{len(ratings)} оценок добавлено'))

        self.stdout.write(self.style.SUCCESS('Заполнение базы данных завершено'))
