# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HttpRequestEntry.priority'
        db.add_column(u'httplog_httprequestentry', 'priority',
                      self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HttpRequestEntry.priority'
        db.delete_column(u'httplog_httprequestentry', 'priority')


    models = {
        u'httplog.httprequestentry': {
            'Meta': {'ordering': "[u'-time']", 'object_name': 'HttpRequestEntry'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'status_code': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['httplog']