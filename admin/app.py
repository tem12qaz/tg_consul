import os
from flask_migrate import Migrate
#from flask_script import Manager
from flask_admin import Admin as Admin_

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

from flask_app_init import app, db

MIGRATION_DIR = os.path.join('admin', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
#manager = Manager(app)


# FLASK-ADMIN
from models import User, Role, TelegramUser, Table, Config, Message, Button, TablePrice, Admin, Priority
from views import HomeAdminView, LogoutView, TelegramUserView, TableView, ButtonView, MessageView, \
    TablePriceView, ConfigView, AdminView, PriorityView

admin = Admin_(app, 'TGbot', url='/admin', index_view=HomeAdminView())

admin.add_view(TelegramUserView(TelegramUser, db.session))
admin.add_view(TableView(Table, db.session))
admin.add_view(PriorityView(Priority, db.session))
admin.add_view(AdminView(Admin, db.session, name='TgAdmin'))
admin.add_view(ConfigView(Config, db.session))
admin.add_view(TablePriceView(TablePrice, db.session))
admin.add_view(MessageView(Message, db.session))
admin.add_view(ButtonView(Button, db.session))

admin.add_view(LogoutView(name='Logout', endpoint='admin/logout_redirect'))

# FLASK-SECURITY
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
