from django.test import TestCase
from apps.core.models import CrudModelEntry
from apps.httplog.models import HttpRequestEntry


class CrudSingalsTest(TestCase):
    """ Tests for core signals """

    def setUp(self):
        self.instance = HttpRequestEntry.objects.create(
            method='GET',
            host='localhost',
            path='/',
            status_code=200
        )

    def test_model_entry_create(self):
        """ Test model signal on creating new instance """
        entry = CrudModelEntry.objects.latest('timestamp')

        self.assertTrue(self.instance.__class__.__name__ in entry.model_name)
        self.assertEquals(entry.instance_id, self.instance.id)
        self.assertEquals(int(entry.action), CrudModelEntry.ACTION_CREATE)

    def test_model_entry_update(self):
        """ Test model signal on updating new instance """

        self.instance.method = 'POST'
        self.instance.save()
        entry = CrudModelEntry.objects.latest('timestamp')

        self.assertTrue(self.instance.__class__.__name__ in entry.model_name)
        self.assertEquals(entry.instance_id, self.instance.id)
        self.assertEquals(int(entry.action), CrudModelEntry.ACTION_UPDATE)

    def test_model_entry_delete(self):
        """ Test model signal on deleting new instance """

        instance_id = self.instance.id
        self.instance.delete()
        entry = CrudModelEntry.objects.latest('timestamp')

        self.assertTrue(self.instance.__class__.__name__ in entry.model_name)
        self.assertEquals(entry.instance_id, instance_id)
        self.assertEquals(int(entry.action), CrudModelEntry.ACTION_DELETE)
