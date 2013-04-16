# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Deploy.status'
        db.alter_column('cruiser_deploy', 'status', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Deploy.finished_at'
        db.alter_column('cruiser_deploy', 'finished_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Deploy.started_at'
        db.alter_column('cruiser_deploy', 'started_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Deploy.status'
        db.alter_column('cruiser_deploy', 'status', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'Deploy.finished_at'
        raise RuntimeError("Cannot reverse this migration. 'Deploy.finished_at' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Deploy.started_at'
        raise RuntimeError("Cannot reverse this migration. 'Deploy.started_at' and its values cannot be restored.")

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cruiser.deploy': {
            'Meta': {'object_name': 'Deploy'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ready'", 'max_length': '16'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cruiser.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_block': ('django.db.models.fields.TextField', [], {'default': "'import fabric'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'repository': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'cruiser.projectparam': {
            'Meta': {'unique_together': "(('project', 'name', 'value'),)", 'object_name': 'ProjectParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Project']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'cruiser.stage': {
            'Meta': {'object_name': 'Stage'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Project']"}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'tasks'", 'symmetrical': 'False', 'through': "orm['cruiser.StageTask']", 'to': "orm['cruiser.Task']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'users'", 'symmetrical': 'False', 'through': "orm['cruiser.StageUser']", 'to': "orm['auth.User']"})
        },
        'cruiser.stageparam': {
            'Meta': {'unique_together': "(('stage', 'name', 'value'),)", 'object_name': 'StageParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'cruiser.stagetask': {
            'Meta': {'object_name': 'StageTask'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Task']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'cruiser.stageuser': {
            'Meta': {'object_name': 'StageUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cruiser.Stage']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cruiser.task': {
            'Meta': {'object_name': 'Task'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['cruiser']