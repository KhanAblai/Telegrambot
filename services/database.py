from peewee import *
psql_db = PostgresqlDatabase('schedules_bot', user='postgres', host='127.0.0.1', password='odikdamix321123')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = psql_db


class Groups(BaseModel):
    name = CharField()


class Users(BaseModel):
    telegram_id = CharField()
    username = CharField()
    group_id = ForeignKeyField(Groups, backref='users',null=True)
    notification = BooleanField()


class Subjects(BaseModel):
    name = CharField()


class Schedules(BaseModel):
    group_id = ForeignKeyField(Groups, backref='schedules')
    day = IntegerField()
    subject_id = ForeignKeyField(Subjects, backref='schedules')
    lesson_start = CharField()
    lesson_end = CharField()


def find_or_create_user(telegram_id):
    try:
        user = Users.get(Users.telegram_id == telegram_id)
        return user
    except DoesNotExist:
        user = Users.create(telegram_id=telegram_id)
        return user


def get_groups():
    return Groups.select()


def save_group_info(telegram_id, group_id):
    user = Users.get(Users.telegram_id == telegram_id)
    user.group_id = group_id
    user.save()

print('База данных инициализирована')
