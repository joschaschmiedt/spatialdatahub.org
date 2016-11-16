from django.test import TestCase

from .base import BaseDatasetTest

from datasets.models import Dataset

from datasets.forms import DatasetForm

from datasets.views import AboutView
from datasets.views import ContactView
from datasets.views import DatasetCreateView
from datasets.views import DatasetDetailView
from datasets.views import DatasetRemoveView
from datasets.views import DatasetUpdateView
from datasets.views import load_dataset
from datasets.views import PortalView

from cryptography.fernet import Fernet
import os



class AboutViewTests(BaseDatasetTest):

    def test_about_url_resolves_to_AboutView(self):
        request = self.factory.get('')
        response = AboutView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_AboutView_uses_correct_template(self):
        response = self.client.get('/about/')
        self.assertTemplateUsed(response,
            template_name="datasets/about.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_AboutView_url_title_is_correct(self):
        response = self.client.get('/about/')
        self.assertIn('<title>ZMT | About</title>', response.content.decode('utf-8'))



class ContactViewTests(BaseDatasetTest):

    def test_ContactView_url_resolves_to_ContactView(self):
        request = self.factory.get('')
        response = ContactView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_ContactView_uses_correct_template(self):
        response = self.client.get('/contact/')
        self.assertTemplateUsed(response,
            template_name="datasets/contact.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_ContactView_url_title_is_correct(self):
        response = self.client.get('/contact/')
        self.assertIn('<title>ZMT | Contact</title>', response.content.decode('utf-8'))



class DatasetCreateViewTests(BaseDatasetTest):

    def test_DatasetCreateView_url_resolves_to_DatasetCreateView(self):
        request = self.factory.get('')
        response = DatasetCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_DatasetCreateView_uses_correct_template(self):
        response = self.client.get('/new_dataset/')
        self.assertTemplateUsed(response,
            template_name="datasets/dataset_create.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_dataset_DatasetCreateView_url_title_is_correct(self):
        response = self.client.get('/new_dataset/')
        self.assertIn('<title>ZMT | Add Dataset</title>', response.content.decode('utf-8'))

    def test_DatasetCreateView_uses_DatasetForm(self):
        response = self.client.get('/new_dataset/')
        self.assertIsInstance(response.context['form'], DatasetForm)



class DatasetDetailViewTests(BaseDatasetTest):

    def test_DatasetDetailView_url_resolves_to_DatasetDetailView(self):
        request = self.factory.get('')
        response = DatasetDetailView.as_view()(request,
                                               slug=self.ds1.slug,
                                               pk=self.ds1.pk)
        self.assertEqual(response.status_code, 200)

    def test_DatasetDetailView_uses_correct_template(self):
        test_url = '/{slug}-{pk}/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertTemplateUsed(response,
            template_name="datasets/dataset_detail.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_DatasetDetailView_url_title_is_correct(self):
        test_url = '/{slug}-{pk}/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertIn('<title>ZMT | %s</title>' % self.ds1.title, response.content.decode('utf-8'))

    def test_dataset_AUTHOR_is_in_the_page(self):
        url = "/{slug}-{pk}/".format(slug=self.ds2.slug, pk=self.ds2.pk)
        response = self.client.get(url)
        self.assertIn(self.ds2.author, response.content.decode("utf-8"))

    def test_dataset_TITLE_is_in_the_page(self):
        url = "/{slug}-{pk}/".format(slug=self.ds2.slug, pk=self.ds2.pk)
        response = self.client.get(url)
        self.assertIn(self.ds2.title, response.content.decode("utf-8"))

    def test_dataset_DESCRIPTION_is_in_the_page(self):
        url = "/{slug}-{pk}/".format(slug=self.ds2.slug, pk=self.ds2.pk)
        response = self.client.get(url)
        self.assertIn(self.ds2.description, response.content.decode("utf-8"))

    def test_password_protected_dataset_does_not_have_user_password_in_final_stage(self):
        url = "/{slug}-{pk}/".format(slug=self.ds3.slug, pk=self.ds3.pk)
        response = self.client.get(url)
        self.assertNotIn(self.ds3.dataset_password, response.content.decode("utf-8"))
        self.assertNotIn(self.ds3.dataset_password, response.context)

    def test_that_DatasetDetailView_brings_in_correct_dataset_object(self):
        url = '/{slug}-{pk}/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(url)
        self.assertEqual(self.ds1, response.context['dataset'])
        self.assertNotEqual(self.ds2, response.context['dataset'])



class DatasetRemoveViewTests(BaseDatasetTest):

    def test_DatasetRemoveView_url_resolves_to_DatasetRemoveView(self):
        request = self.factory.get('')
        response = DatasetRemoveView.as_view()(request,
                                               slug=self.ds1.slug,
                                               pk=self.ds1.pk)
        self.assertEqual(response.status_code, 200)

    def test_DatasetRemoveView_uses_correct_template(self):
        test_url = '/{slug}-{pk}/remove/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertTemplateUsed(response,
            template_name="datasets/dataset_remove.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_DatasetRemoveView_url_title_is_correct(self):
        test_url = '/{slug}-{pk}/remove/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertIn('<title>ZMT | Remove Dataset</title>', response.content.decode('utf-8'))

    def test_that_DatasetRemoveView_brings_in_correct_dataset_object(self):
        test_url = '/{slug}-{pk}/remove/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertEqual(self.ds1, response.context['dataset'])
        self.assertNotEqual(self.ds2, response.context['dataset'])


class DatasetUpdateViewTests(BaseDatasetTest):

    def test_DatasetUpdateView_url_resolves_to_DatasetUpdateView(self):
        request = self.factory.get('')
        response = DatasetUpdateView.as_view()(request,
                                               slug=self.ds1.slug,
                                               pk=self.ds1.pk)
        self.assertEqual(response.status_code, 200)

    def test_DatasetUpdateView_url_title_is_correct(self):
        test_url = '/{slug}-{pk}/update/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertIn('<title>ZMT | Update %s</title>' % self.ds1.title, response.content.decode('utf-8'))

    def test_DatasetUpdateView_uses_correct_template(self):
        test_url = '/{slug}-{pk}/update/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertTemplateUsed(response, template_name="datasets/dataset_update.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_that_DatasetUpdateView_brings_in_correct_dataset_object(self):
        test_url = '/{slug}-{pk}/update/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertEqual(self.ds1, response.context['dataset'])
        self.assertNotEqual(self.ds2, response.context['dataset'])

    def test_that_DatasetUpdateView_uses_DatasetForm(self):
        test_url = '/{slug}-{pk}/update/'.format(slug=self.ds1.slug, pk=self.ds1.pk)
        response = self.client.get(test_url)
        self.assertIsInstance(response.context['form'], DatasetForm)



class LoadDatasetViewTests(BaseDatasetTest):

    """
    The test client returns an HttpResponse object that is actually not the
    same as the HttpRequest response object.
    The only reason to use the test client would be to use the other
    arguements, such as content, context, json, etc.
    """

    def test_load_dataset_returns_status_code_200(self):
        test_url = '/load_dataset/{pk}/'.format(pk=self.ds2.pk)
        response = self.client.get(test_url)
        self.assertEqual(200, response.status_code)

    def test_load_dataset_returns_status_code_200_PASSWORD_PROTECTED(self):
        test_url = '/load_dataset/{pk}/'.format(pk=self.ds3.pk)
        response = self.client.get(test_url)
        self.assertEqual(200, response.status_code)

    def test_load_dataset_returns_content(self):
        test_url = '/load_dataset/{pk}/'.format(pk=self.ds2.pk)
        response = self.client.get(test_url)
        self.assertIn(b'properties', response.content)

    """
    def test_load_dataset_returns_content_PASSWORD_PROTECTED(self):
        test_url = '/load_dataset/{pk}/'.format(pk=self.ds3.pk)

        cryptokey = os.environ['CRYPTOKEY'].encode('UTF-8')
        cryptokey_fernet = Fernet(cryptokey)

        password_bytes = (self.ds3.dataset_password).encode('UTF-8')
        password_decrypted_bytes = cryptokey_fernet.decrypt(password_bytes)
        password_decrypted_string = password_decrypted_bytes.decode('UTF-8')

        user_bytes = (self.ds3.dataset_user).encode('UTF-8')
        user_decrypted_bytes = cryptokey_fernet.decrypt(user_bytes)
        user_decrypted_string = user_decrypted_bytes.decode('UTF-8')

        print('''the methods for encrypting and decrypting work, but i cant get
any content from the page for one reason or another''')
        print(self.ds3.dataset_password)
        print(self.ds3.dataset_user)
        print(password_decrypted_string)
        print(user_decrypted_string)

        response = self.client.get(test_url)
        self.assertIn(b'properties', response.content)
    """



class PortalViewTestsThatRequireData_EMPTY_DATABASE(TestCase):

    def test_that_PortalView_without_datasets_says_none_available(self):
        response = self.client.get('/')
        self.assertIn('There are no datasets available',
            response.content.decode('utf-8'))

    def test_that_PortalView_brings_in_correct_number_of_dataset_objects(self):
        response = self.client.get('/')
        self.assertEqual(0, len(response.context['dataset_list']))


class PortalViewTestsThatRequireData(BaseDatasetTest):

    def test_base_url_resolves_to_PortalView(self):
        request = self.factory.get('')
        response = PortalView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_PortalView_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,
            template_name="datasets/portal.html")
        self.assertTemplateUsed(response,
            template_name="base.html")

    def test_PortalView_title_is_correct(self):
        response = self.client.get('/')
        self.assertIn('<title>ZMT | GIS Portal</title>', response.content.decode('utf-8'))

    def test_that_PortalView_brings_in_correct_number_of_dataset_objects(self):
        response = self.client.get('/')
        self.assertEqual(3, len(response.context['dataset_list']))

    def test_that_PortalView_brings_in_correct_list_of_dataset_objects(self):
        response = self.client.get('/')
        object_list = Dataset.objects.all()
        for index, ds in enumerate(object_list):
            self.assertEqual(ds, response.context['dataset_list'][index])

    def test_PortalView_search_function(self):
        """
        This will be refactoed to use an ajax call
        """

        # Use the set up from the tests file in the datasets app
        # then filter them and check
        dataset_list = Dataset.objects.filter(title__contains=('ZMT'))
        self.assertEqual(len(dataset_list), 1)

        # now run it as a get request for "zmt"
        response = self.client.get('/?q=zmt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('ZMT GeoJSON Polygon', response.content.decode('utf-8'))
        self.assertNotIn('Mapbox GeoJson Example', response.content.decode('utf-8'))
