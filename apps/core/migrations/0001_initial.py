# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CrudModelEntry'
        db.create_table(u'core_crudmodelentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('instance_id', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['CrudModelEntry'])


    def backwards(self, orm):
        # Deleting model 'CrudModelEntry'
        db.delete_table(u'core_crudmodelentry')


    models = {
        u'core.crudmodelentry': {
            'Meta': {'object_name': 'CrudModelEntry'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_id': ('django.db.models.fields.IntegerField', [], {}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']