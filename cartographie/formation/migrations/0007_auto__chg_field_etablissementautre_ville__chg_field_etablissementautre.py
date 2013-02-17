# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'EtablissementAutre.ville'
        db.alter_column('formation_etablissementautre', 'ville', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'EtablissementAutre.url'
        db.alter_column('formation_etablissementautre', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'EtablissementAutre.pays'
        db.alter_column('formation_etablissementautre', 'pays_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['references.Pays'], null=True))

        # Changing field 'EtablissementAutre.nom_origine'
        db.alter_column('formation_etablissementautre', 'nom_origine', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'EtablissementAutre.sigle'
        db.alter_column('formation_etablissementautre', 'sigle', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

    def backwards(self, orm):

        # Changing field 'EtablissementAutre.ville'
        db.alter_column('formation_etablissementautre', 'ville', self.gf('django.db.models.fields.CharField')(default=None, max_length=150))

        # Changing field 'EtablissementAutre.url'
        db.alter_column('formation_etablissementautre', 'url', self.gf('django.db.models.fields.URLField')(default=None, max_length=200))

        # Changing field 'EtablissementAutre.pays'
        db.alter_column('formation_etablissementautre', 'pays_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['references.Pays']))

        # Changing field 'EtablissementAutre.nom_origine'
        db.alter_column('formation_etablissementautre', 'nom_origine', self.gf('django.db.models.fields.CharField')(default=None, max_length=150))

        # Changing field 'EtablissementAutre.sigle'
        db.alter_column('formation_etablissementautre', 'sigle', self.gf('django.db.models.fields.CharField')(default=None, max_length=150))

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
        'formation.acces': {
            'Meta': {'object_name': 'Acces'},
            'active': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Etablissement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'formation.delivrancediplome': {
            'Meta': {'object_name': 'DelivranceDiplome', 'db_table': "'formation_config_delivrancediplome'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.discipline': {
            'Meta': {'object_name': 'Discipline', 'db_table': "'formation_config_discipline'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Discipline']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.etablissementautre': {
            'Meta': {'object_name': 'EtablissementAutre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'nom_origine': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Pays']", 'null': 'True', 'blank': 'True'}),
            'sigle': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        'formation.etablissementcomposante': {
            'Meta': {'object_name': 'EtablissementComposante'},
            'diplomante': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Etablissement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'nom_origine': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Pays']", 'null': 'True', 'blank': 'True'}),
            'sigle': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        'formation.formation': {
            'Meta': {'object_name': 'Formation'},
            'commentaires': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'commentaires+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.FormationCommentaire']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'contacts+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.Personne']"}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {}),
            'delivrance_diplome': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['formation.DelivranceDiplome']"}),
            'discipline_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['formation.Discipline']"}),
            'discipline_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['formation.Discipline']"}),
            'discipline_3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['formation.Discipline']"}),
            'duree': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Etablissement']"}),
            'etablissement_composante': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'to': "orm['formation.EtablissementComposante']", 'through': "orm['formation.FormationComposante']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'etablissement_emet_diplome': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'langue': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'langue+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.Langue']"}),
            'modifications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'modifications+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.FormationModification']"}),
            'niveau_diplome': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['formation.NiveauDiplome']"}),
            'niveau_entree': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'niveau_entree+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.NiveauUniversitaire']"}),
            'niveau_sortie': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'niveau_sortie+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.NiveauUniversitaire']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'nom_origine': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'partenaires_auf': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'to': "orm['references.Etablissement']", 'through': "orm['formation.FormationPartenaireAUF']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'partenaires_autres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'to': "orm['formation.EtablissementAutre']", 'through': "orm['formation.FormationPartenaireAutre']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'presentation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'responsables': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'responsables+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.Personne']"}),
            'sigle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type_diplome': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['formation.TypeDiplome']"}),
            'type_formation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'type_formation+'", 'null': 'True', 'to': "orm['formation.TypeFormation']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vocation': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'vocation+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['formation.Vocation']"})
        },
        'formation.formationcommentaire': {
            'Meta': {'object_name': 'FormationCommentaire'},
            'commentaire': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'formation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['formation.Formation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_display': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.formationcomposante': {
            'Meta': {'object_name': 'FormationComposante'},
            'etablissementComposante': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['formation.EtablissementComposante']"}),
            'etablissement_composante_emet_diplome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'formation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['formation.Formation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'formation.formationmodification': {
            'Meta': {'ordering': "['-date']", 'object_name': 'FormationModification'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'formation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['formation.Formation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'formation.formationpartenaireauf': {
            'Meta': {'object_name': 'FormationPartenaireAUF'},
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['references.Etablissement']"}),
            'formation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['formation.Formation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partenaire_auf_emet_diplome': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'formation.formationpartenaireautre': {
            'Meta': {'object_name': 'FormationPartenaireAutre'},
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['formation.EtablissementAutre']"}),
            'formation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['formation.Formation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partenaire_autre_emet_diplome': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'formation.langue': {
            'Meta': {'object_name': 'Langue', 'db_table': "'formation_config_langue'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.niveaudiplome': {
            'Meta': {'object_name': 'NiveauDiplome', 'db_table': "'formation_config_niveaudiplome'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.niveauuniversitaire': {
            'Meta': {'object_name': 'NiveauUniversitaire', 'db_table': "'formation_config_niveauuniversitaire'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.personne': {
            'Meta': {'object_name': 'Personne'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Etablissement']"}),
            'fonction': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'formation.typediplome': {
            'Meta': {'object_name': 'TypeDiplome', 'db_table': "'formation_config_typediplome'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.typeformation': {
            'Meta': {'object_name': 'TypeFormation', 'db_table': "'formation_config_typeformation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'formation.userrole': {
            'Meta': {'object_name': 'UserRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'roles'", 'symmetrical': 'False', 'to': "orm['references.Region']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['auth.User']"})
        },
        'formation.vocation': {
            'Meta': {'object_name': 'Vocation', 'db_table': "'formation_config_vocation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'references.bureau': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Bureau', 'db_table': "u'ref_bureau'", 'managed': 'False'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Implantation']", 'db_column': "'implantation'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Region']", 'db_column': "'region'"})
        },
        'references.discipline': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Discipline', 'db_table': "u'ref_discipline'", 'managed': 'False'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'references.etablissement': {
            'Meta': {'ordering': "['pays__nom', 'nom']", 'object_name': 'Etablissement', 'db_table': "u'ref_etablissement'", 'managed': 'False'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cedex': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'historique': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'db_column': "'implantation'", 'to': "orm['references.Implantation']"}),
            'membre': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'membre_adhesion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nombre_chercheurs': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre_enseignants': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre_etudiants': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre_membres': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to_field': "'code'", 'db_column': "'pays'", 'to': "orm['references.Pays']"}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'qualite': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'db_column': "'region'", 'to': "orm['references.Region']"}),
            'responsable_courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'responsable_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsable_genre': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'responsable_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsable_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sigle': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'statut': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'references.implantation': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Implantation', 'db_table': "u'ref_implantation'", 'managed': 'False'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adresse_physique_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'adresse_physique_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_physique'", 'to_field': "'code'", 'db_column': "'adresse_physique_pays'", 'to': "orm['references.Pays']"}),
            'adresse_physique_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adresse_postale_boite_postale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'adresse_postale_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_postale'", 'to_field': "'code'", 'db_column': "'adresse_postale_pays'", 'to': "orm['references.Pays']"}),
            'adresse_postale_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Implantation']", 'db_column': "'bureau_rattachement'"}),
            'code_meteo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'courriel_interne': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'date_extension': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_inauguration': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fuseau_horaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hebergement_convention': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_convention_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_etablissement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modif_date': ('django.db.models.fields.DateField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Region']", 'db_column': "'region'"}),
            'remarque': ('django.db.models.fields.TextField', [], {}),
            'responsable_implantation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'statut': ('django.db.models.fields.IntegerField', [], {}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'zone_administrative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.ZoneAdministrative']"})
        },
        'references.pays': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Pays', 'db_table': "u'ref_pays'", 'managed': 'False'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'code_bureau': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Bureau']", 'to_field': "'code'", 'null': 'True', 'db_column': "'code_bureau'", 'blank': 'True'}),
            'code_iso3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'developpement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monnaie': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nord_sud': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Region']", 'db_column': "'region'"})
        },
        'references.region': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Region', 'db_table': "u'ref_region'", 'managed': 'False'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation_bureau': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gere_region'", 'null': 'True', 'db_column': "'implantation_bureau'", 'to': "orm['references.Implantation']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'references.zoneadministrative': {
            'Meta': {'ordering': "['nom']", 'object_name': 'ZoneAdministrative', 'db_table': "'ref_zoneadministrative'", 'managed': 'False'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['formation']