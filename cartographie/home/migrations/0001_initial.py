# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FeedbackProfil'
        db.create_table('home_feedbackprofil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('home', ['FeedbackProfil'])

        # Adding model 'Feedback'
        db.create_table('home_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courriel', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('prenom', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('profil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.FeedbackProfil'], null=True, blank=True)),
            ('profil_autre', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('date_envoi', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('sujet', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('contenu', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('home', ['Feedback'])


    def backwards(self, orm):
        # Deleting model 'FeedbackProfil'
        db.delete_table('home_feedbackprofil')

        # Deleting model 'Feedback'
        db.delete_table('home_feedback')


    models = {
        'home.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'date_envoi': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.FeedbackProfil']", 'null': 'True', 'blank': 'True'}),
            'profil_autre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sujet': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        'home.feedbackprofil': {
            'Meta': {'object_name': 'FeedbackProfil'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['home']