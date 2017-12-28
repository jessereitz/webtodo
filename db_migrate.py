#!flask/bin/python
import imp
from migrate.versioning import api
from app import db
from config import Config

SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = Config.SQLALCHEMY_MIGRATE_REPO

# current version
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (version + 1))

tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

exec(old_model, tmp_module.__dict__)

# create and write a migration script. Useful for post-migration checking.
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, 'wt').write(script)

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# new version
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('\n')
print('New migration saved as ' + migration)
print('Current database version: ' + str(version))
