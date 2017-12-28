from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=64), nullable=False),
    Column('note', String(length=140)),
    Column('complete', Boolean, nullable=False),
    Column('user_id', Integer, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['complete'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['complete'].drop()
