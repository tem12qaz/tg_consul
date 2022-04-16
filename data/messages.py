SELECT_LANG_MESSAGE = 'Choose language/Выберите язык:'
CART_ROW = '''{num} {name} (category)
{price} VND x {count} = {sum} VND

'''
ORDER_SHOP_MESSAGE = '''
Order #{id_}
User @{username}
Service <b>{name_ru}/{name_en}</b>
'''

MESSAGE = '''<code>{time}</code> <b>{name}</b>
{text}

'''


class Ru:
    BOT_MEESAGE = 'Информация о боте'
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
    SELECT_REST_MESSAGE = 'Выберите ресторан:'
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
    INPUT_ADDRESS_MESSAGE = 'Отправьте свою геолокацию или напишите адрес'
    USE_OLD_ADDRESS_MESSAGE = 'Использовать данные для доставки, которые были при прошлом заказе?'
    SELECT_TIME_MESSAGE = 'Укажите время доставки:'
    SELECT_AREA_MESSAGE = 'Выберите район доставки'
    ADDRESS_APPS_MESSAGE = 'Дополнения к адресу (название отеля, номер дома и т.д). Дополнения лучше писать на английском языке, если вы заказываете не из ресторана русской кухни'
    NAME_MESSAGE = 'Как вас зовут?'
    COMMUNICATION_MESSAGE = 'Укажите, как с вами связаться для подтверждения заказа'
    PHONE_MESSAGE = 'Пожалуйста, напишите ваш телефонный номер'
    WHATSAPP_MESSAGE = 'Пожалуйста, напишите номер вашего WhatsApp в международном формате (11 цифр и + в начале)'
    SERVICE_ORDER_MESSAGE = '''Ваш заказ #{id_} принят и отправлен в обработку! В ближайшее время магазин свяжется с вами для подтверждения.'''
    ORDER_MESSAGE = '''Ваш заказ #{id_} принят и отправлен в обработку! В ближайшее время ресторан свяжется с вами для подтверждения. Вот состав вашей корзины:

<code>{rows}</code>
Доставка: {delivery} VND
Итого: {sum} VND'

Отправьте /chat{id_} для чата с рестораном
'''
    REST_ORDER_MESSAGE = '''Order #{id_}:
    
Name: {name}
Language: {lang}
Communication: {communication}
Delivery time: {time}
Address: {address}

<code>{rows}</code>
Delivery: {delivery} VND
Total: {sum} VND'

Send /chat{id_} to chat with user
'''
    CHAT_MESSAGE = '''Чат по заказу #{id_}

{messages}

Отправьте /exit для выхода из чата'''


class En:
    BOT_MESSAGE = 'Bot info'

    START_MESSAGE = 'Select category'
    SELECT_CATEGORY = 'Select category'
    SELECTED_KITCHEN_MESSAGE = '''Selected cuisine: <b>{name}</b>

Choose the restaurant:'''
    SELECT_REST_MESSAGE = 'Select restaurant:'
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
    INPUT_ADDRESS_MESSAGE = 'Send your location or shipping address'
    USE_OLD_ADDRESS_MESSAGE = 'Should I use the delivery data that was with the previous order?'
    SELECT_TIME_MESSAGE = 'Delivery time:'
    SELECT_AREA_MESSAGE = 'Select delivery area'
    ADDRESS_APPS_MESSAGE = 'Additional information about your address if you have (hotel name, number of your house, etc)'
    NAME_MESSAGE = 'Please send you name'
    COMMUNICATION_MESSAGE = 'How to contact you to confirm the order'
    PHONE_MESSAGE = 'Enter your phone number'
    WHATSAPP_MESSAGE = 'Enter your WhatsApp number in international format with plus in front of number'
    SERVICE_ORDER_MESSAGE = '''We got your order #{id_}.
The shop will contact you shortly to confirm it.'''
    ORDER_MESSAGE = '''We got your order #{id_}.
The restaurant will contact you shortly to confirm it. :

<code>{rows}</code>
Delivery: {delivery} VND
Total payable: {sum} VND

Send /chat{id_} to chat with the restaurant
'''
    REST_ORDER_MESSAGE = '''Order #{id_}:

    Username: @{username}
    Name: {name}
    Communication: {communication}
    Delivery time: {time}
    Address: {address}

    <code>{rows}</code>
    Delivery: {delivery} VND
    Total: {sum} VND'

    Send /chat{id_} to 
'''
    CHAT_MESSAGE = '''Chat  Order #{id_}

{messages}

Send /exit to leave the chat
'''
