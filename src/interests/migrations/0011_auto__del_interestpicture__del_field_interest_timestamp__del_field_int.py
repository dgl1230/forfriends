# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'InterestPicture'
        db.delete_table(u'interests_interestpicture')

        # Deleting field 'Interest.timestamp'
        db.delete_column(u'interests_interest', 'timestamp')

        # Deleting field 'Interest.update'
        db.delete_column(u'interests_interest', 'update')

        # Deleting field 'Interest.for_new_users'
        db.delete_column(u'interests_interest', 'for_new_users')

        # Deleting field 'Category.updated'
        db.delete_column(u'interests_category', 'updated')

        # Deleting field 'Category.timestamp'
        db.delete_column(u'interests_category', 'timestamp')

        # Deleting field 'Category.slug'
        db.delete_column(u'interests_category', 'slug')

        # Deleting field 'UserInterestAnswer.timestamp'
        db.delete_column(u'interests_userinterestanswer', 'timestamp')

        # Deleting field 'UserInterestAnswer.update'
        db.delete_column(u'interests_userinterestanswer', 'update')

        # Deleting field 'UserInterestAnswer.importance_level'
        db.delete_column(u'interests_userinterestanswer', 'importance_level')


    def backwards(self, orm):
        # Adding model 'InterestPicture'
        db.create_table(u'interests_interestpicture', (
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('interest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interests.Interest'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'interests', ['InterestPicture'])


        # User chose to not deal with backwards NULL issues for 'Interest.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'Interest.timestamp' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Interest.timestamp'
        db.add_column(u'interests_interest', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Interest.update'
        raise RuntimeError("Cannot reverse this migration. 'Interest.update' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Interest.update'
        db.add_column(u'interests_interest', 'update',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)

        # Adding field 'Interest.for_new_users'
        db.add_column(u'interests_interest', 'for_new_users',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Category.updated'
        raise RuntimeError("Cannot reverse this migration. 'Category.updated' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Category.updated'
        db.add_column(u'interests_category', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Category.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'Category.timestamp' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Category.timestamp'
        db.add_column(u'interests_category', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Category.slug'
        raise RuntimeError("Cannot reverse this migration. 'Category.slug' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Category.slug'
        db.add_column(u'interests_category', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=50),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'UserInterestAnswer.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'UserInterestAnswer.timestamp' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserInterestAnswer.timestamp'
        db.add_column(u'interests_userinterestanswer', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'UserInterestAnswer.update'
        raise RuntimeError("Cannot reverse this migration. 'UserInterestAnswer.update' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserInterestAnswer.update'
        db.add_column(u'interests_userinterestanswer', 'update',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)

        # Adding field 'UserInterestAnswer.importance_level'
        db.add_column(u'interests_userinterestanswer', 'importance_level',
                      self.gf('django.db.models.fields.CharField')(default='Neutral', max_length=20, null=True, blank=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'interests.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['interests.Interest']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'interests.interest': {
            'Meta': {'object_name': 'Interest'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'interests.userinterestanswer': {
            'Meta': {'object_name': 'UserInterestAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interests.Interest']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['interests']