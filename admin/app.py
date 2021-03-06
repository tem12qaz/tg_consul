import os
from flask_migrate import Migrate
#from flask_script import Manager
from flask_admin import Admin as Admin_

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

from models import User, Role, Account, Proxy, Config, City
from views import HomeAdminView, LogoutView, AccountView, ProxyView, ConfigView, CityView
from flask_app_init import app, db

MIGRATION_DIR = os.path.join('admin', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
#manager = Manager(app)

# FLASK-ADMIN

admin = Admin_(app, 'TGbot', url='/admin', index_view=HomeAdminView())

admin.add_view(AccountView(Account, db.session))
admin.add_view(ProxyView(Proxy, db.session))
admin.add_view(ConfigView(Config, db.session))
admin.add_view(CityView(City, db.session))

admin.add_view(LogoutView(name='Logout', endpoint='admin/logout_redirect'))

# FLASK-SECURITY
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
