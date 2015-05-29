# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Userinfo.job' to match new field type.
        db.rename_column(u'userinfo', 'job', 'job_id')
        # Changing field 'Userinfo.job'
        db.alter_column(u'userinfo', 'job_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['engine.Job']))
        # Adding index on 'Userinfo', fields ['job']
        db.create_index(u'userinfo', ['job_id'])


    def backwards(self, orm):
        # Removing index on 'Userinfo', fields ['job']
        db.delete_index(u'userinfo', ['job_id'])


        # Renaming column for 'Userinfo.job' to match new field type.
        db.rename_column(u'userinfo', 'job_id', 'job')
        # Changing field 'Userinfo.job'
        db.alter_column(u'userinfo', 'job', self.gf('django.db.models.fields.CharField')(max_length=128))

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
        'engine.alarminfo': {
            'Meta': {'object_name': 'Alarminfo', 'db_table': "u'alarminfo'"},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'suggestion': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alarm_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.blackemail': {
            'Meta': {'object_name': 'BlackEmail', 'db_table': "u'black_email'"},
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'emailtype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'reip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'riskvalue': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blackemail_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.blackip': {
            'Meta': {'object_name': 'BlackIp', 'db_table': "u'black_ip'"},
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'iptype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'reip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'riskvalue': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blackip_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.blacktrojan': {
            'Meta': {'object_name': 'BlackTrojan', 'db_table': "u'black_trojan'"},
            'begin': ('django.db.models.fields.IntegerField', [], {}),
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'feature': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'reip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blacktrojan_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.blackurl': {
            'Meta': {'object_name': 'BlackUrl', 'db_table': "u'black_url'"},
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'reip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'riskvalue': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'urltype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blackurl_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.job': {
            'Meta': {'object_name': 'Job', 'db_table': "u'job'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'pid': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['engine.Job']", 'null': 'True'})
        },
        'engine.login': {
            'Meta': {'object_name': 'Login', 'db_table': "u'login'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'login_userid'", 'to': "orm['engine.Userinfo']"}),
            'userip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        'engine.questions': {
            'Meta': {'object_name': 'Questions', 'db_table': "u'questions'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'engine.resemail': {
            'Meta': {'object_name': 'ResEmail', 'db_table': "u'res_email'"},
            'alarm': ('django.db.models.fields.CharField', [], {'default': "'00'", 'max_length': '2'}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'dip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dport': ('django.db.models.fields.IntegerField', [], {}),
            'emailtype': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifalarmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'iswhite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'receiver': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'riskvalue': ('django.db.models.fields.IntegerField', [], {}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'sport': ('django.db.models.fields.IntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resemail_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.resip': {
            'Meta': {'object_name': 'ResIp', 'db_table': "u'res_ip'"},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'dip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dport': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifalarmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'iptype': ('django.db.models.fields.IntegerField', [], {}),
            'iswhite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'riskvalue': ('django.db.models.fields.IntegerField', [], {}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'sport': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resip_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.restrojan': {
            'Meta': {'object_name': 'ResTrojan', 'db_table': "u'res_trojan'"},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'dip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dport': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifalarmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'receiver': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'sport': ('django.db.models.fields.IntegerField', [], {}),
            'trojan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'restrojan_balcktrojanid'", 'to': "orm['engine.BlackTrojan']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'restrojan_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.resurl': {
            'Meta': {'object_name': 'ResUrl', 'db_table': "u'res_url'"},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deal': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'dip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dport': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifalarmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'iswhite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'riskvalue': ('django.db.models.fields.IntegerField', [], {}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'sport': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'urltype': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resurl_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.userinfo': {
            'Meta': {'object_name': 'Userinfo', 'db_table': "u'userinfo'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idnum': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'idpic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['engine.Job']"}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'riskvalue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'workplace': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'engine.whiteemail': {
            'Meta': {'object_name': 'WhiteEmail', 'db_table': "u'white_email'"},
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whiteemail_blackemailid'", 'to': "orm['engine.BlackEmail']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whiteemail_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.whiteip': {
            'Meta': {'object_name': 'WhiteIp', 'db_table': "u'white_ip'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whiteip_blackipid'", 'to': "orm['engine.BlackIp']"}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whiteip_userid'", 'to': "orm['engine.Userinfo']"})
        },
        'engine.whiteurl': {
            'Meta': {'object_name': 'WhiteUrl', 'db_table': "u'white_url'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whiteurl_blackurlid'", 'to': "orm['engine.BlackUrl']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whiteurl_userid'", 'to': "orm['engine.Userinfo']"})
        }
    }

    complete_apps = ['engine']