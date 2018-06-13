from django.test import TestCase
from .models import Category, Article, Comment, User
from .forms import CommentForm
# Create your tests here.


class CategoryModelTest(TestCase):

    def test_string_representation(self):
        category = Category(category_name="Test Category")
        self.assertEqual(str(category), category.category_name)


class ArticleModelTest(TestCase):

    def test_string_representation(self):
        article = Article(title="Test Article")
        self.assertEqual(str(article), article.title)


class CommentModelTest(TestCase):

    def test_string_representation(self):
        comment = Comment(comment_author="Test User", comment_content="Test Contentent")
        self.assertEqual(str(comment), "Test User: Test Contentent")


class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ArticleViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name="Test Category")
        self.article = Article.objects.create(title='test-title', url_title='test-url-title', content='test-body',
                                              date_pub='2018-01-01', active=True, category_article_id=self.category,
                                              author=user)

    def test_basic_view(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class CommentFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(category_name="Test Category")
        self.article = Article.objects.create(id=1, title='test-title', url_title='test-url-title', content='test-body',
                                              date_pub='2018-01-01', active=True, category_article_id=self.category,
                                              author=self.user)

    def test_valid_data(self):
        form = CommentForm(data={
            'add_date': '2018-06-13',
            'comment_author': "test comment autor",
            'comment_content': "comment content",
            'post': self.article.id
        })
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = CommentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'comment_author': [u'This field is required.'],
            'comment_content': [u'This field is required.'],
            'post': [u'This field is required.']
        })

