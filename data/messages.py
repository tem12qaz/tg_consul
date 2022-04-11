SELECT_LANG_MESSAGE = 'Choose language/Выберите язык:'
CART_ROW = '''{num} {name} (category)
{price} VND x {count} = {sum} VND
'''


class Ru:
    START_MESSAGE = 'Выберете раздел'
    SELECT_CATEGORY = 'Выберете категорию'
    SELECTED_KITCHEN_MESSAGE = '''Выбранная кухня: <b>{name}</b>

Выберите ресторан:'''
    REST_MESSAGE = '''<b>{name}</b>
{description}
Минимальная сумма заказа: {min_price} VND
Стоимость доставки: {delivery} VND
Время работы: {time}

Выберите категорию блюда:
'''
    PRODUCT_MESSAGE = '''Ресторан: <b>{rest}</b>

<b>{name}</b>
{description}
Цена: {price}VND
'''
    ORDER_EXISTING_MESSAGE = '''В вашей корзине уже есть заказ. Нажмите Корзина 🛒, чтобы перейти к его оформлению или Очистить корзину 🏃‍♂️, чтобы очистить корзину и начать заказ заново.'''
    SELECT_DISH_MESSAGE = 'Выбери одно из блюд'
    CART_MESSAGE = '''{rest}

{rows}

Итого: <b>{sum}</b> VND
Доставка: {delivery} VND

Нажмите Подтвердить ✅ для подтверждения заказа, а если вы хотите удалить одно из блюд, нажмите ❌'''
    CART_EMPTY_MESSAGE = 'Ваша корзина пуста. Нажмите кнопку "Главное меню 🏠" в самом низу, чтобы перейти к выбору кухни.'
    SERVICE_TYPE_MESSAGE = '''<b>{name}</b>
Выберете тип услуги'''
    SERVICE_SHOP_MESSAGE = '''<b>{name}</b>
{description}'''


class En:
    START_MESSAGE = 'Select category'
    SELECT_CATEGORY = 'Select category'
    SELECTED_KITCHEN_MESSAGE = '''Selected cuisine: <b>{name}</b>

Choose the restaurant:'''
    REST_MESSAGE = '''<b>{name}</b>
{description}
Minimal order: {min_price}VND
Delivery cost: {delivery}VND
Working hours: {time}

Choose the dish category:
'''
    PRODUCT_MESSAGE = '''Restaurant: <b>{rest}</b>
    
<b>{name}</b>
{description}
Price: {price}VND
'''
    ORDER_EXISTING_MESSAGE = '''There is already an order in your cart. Press Cart 🛒 to proceed to checkout or press Remove order 🏃‍♂️ to remove order'''
    SELECT_DISH_MESSAGE = 'Select one of top dishes'
    CART_MESSAGE = '''{rest}

{rows}

Subtotal: <b>{sum}</b> VND
Delivery cost: {delivery} VND

Press Confirm your order ✅ to continue or ❌ to remove one of the dishes'''
    CART_EMPTY_MESSAGE = 'Your cart is empty. Please press "Home 🏠" button to make an order'
    SERVICE_TYPE_MESSAGE = '''<b>{name}</b>
Select service type'''
    SERVICE_SHOP_MESSAGE = '''<b>{name}</b>
{description}'''


