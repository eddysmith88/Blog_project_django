from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Profile, Post, Comment
from django.urls import reverse


class CategoryTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEquals(category.get_absolute_url(), reverse('home'))


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.create(user=user, bio='Test Bio')

    def test_bio_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'bio')

    def test_bio_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('bio').max_length
        self.assertEquals(max_length, None)  # Since it's a TextField


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        Post.objects.create(title='Test Post', author=user, snippet='Test Snippet')

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        post = Post.objects.create(title='Test Post', author=user, snippet='Test Snippet')
        Comment.objects.create(post=post, name='Test Name', body='Test Body')

    def test_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)
