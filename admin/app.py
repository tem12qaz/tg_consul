import os
from flask_migrate import Migrate
#from flask_script import Manager
from flask_admin import Admin

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

from flask_app_init import app, db

MIGRATION_DIR = os.path.join('admin', 'migrations')

migrate = Migrate(app, db, directory=MIGRATION_DIR)
#manager = Manager(app)


# FLASK-ADMIN
from models import User, Role, ServiceShop, ServiceCategory, MealCategory, Service, Restaurant, RestaurantCategory, \
    Product, Order, ServiceOrder
from views import HomeAdminView, ServiceCategoryView, LogoutView, ServiceShopView, ServiceView, MealCategoryView, \
    RestaurantView, RestaurantCategoryView, ProductView, ServiceOrderView, OrderView

admin = Admin(app, 'TGbot', url='/admin', index_view=HomeAdminView())

admin.add_view(ServiceCategoryView(ServiceCategory, db.session))
admin.add_view(ServiceShopView(ServiceShop, db.session))
admin.add_view(ServiceView(Service, db.session))
admin.add_view(MealCategoryView(MealCategory, db.session))
admin.add_view(RestaurantView(Restaurant, db.session))
admin.add_view(RestaurantCategoryView(RestaurantCategory, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(OrderView(Order, db.session))
admin.add_view(ServiceOrderView(ServiceOrder, db.session))

admin.add_view(LogoutView(name='Logout', endpoint='admin/logout_redirect'))

# FLASK-SECURITY
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
