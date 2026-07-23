from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, ConversationHandler, \
CallbackContext
import db

TOKEN = 'TOKEN'

(
    NAME,
    PHONE,
    LOCATION,
    MAIN_MENU,
    EDIT_NAME,
    EDIR_PHONE,
    SETTINGS_MENU,
    FOOD_MENU
) = range(8)


def start(update: Update, context: CallbackContext):
    user = db.get_user(update.effective_user.id)

    if user:
        return main_menu(update, context)

    update.message.reply_text("👤 Ism Familya kiriting: ")
    return NAME


def get_name(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text("📞 Telefon raqamingizni yuboring: ",
                              reply_markup=ReplyKeyboardMarkup(
                                  [[KeyboardButton("Raqamingizni kiriting 📱", request_contact=True)]],
                                  resize_keyboard=True
                              ))
    return PHONE


def get_phone(update, context):
    context.user_data['phone'] = update.message.contact.phone_number
    update.message.reply_text("📍 Manzilingizni kiriting: ",
                              reply_markup=ReplyKeyboardMarkup(
                                  [[KeyboardButton("📍 Manzilingizni yuborish", request_location=True)]],
                                  resize_keyboard=True
                              ))
    return LOCATION


def get_location(update, context):
    loc = update.message.location

    db.add_user(
        update.effective_user.id,
        context.user_data['name'],
        context.user_data['phone'],
        loc.latitude,
        loc.longitude
    )

    update.message.reply_text("Ro'yhatdan o'tdingiz ✅")
    return main_menu(update, context)





def main_menu(update, context):
    update.message.reply_text("Asosiy menu: ",
                              reply_markup=ReplyKeyboardMarkup(
                                  [
                                      ["📋 Menyu", "🛒 Savat"],
                                      ["⚙️ Sozlamalar"],
                                      ["💬 Izoh qoldirish"]
                                  ],
                                  resize_keyboard=True
                              ))
    return MAIN_MENU


def main_menu_select(update, context):
    text = update.message.text

    if text == "📋 Menyu":
        return food_menu(update, context)
    elif text == "⚙️ Sozlamalar":
        return settings_menu(update, context)
    elif text == "💬 Izoh qoldirish":
        update.message.reply_text("Izoh yozish mumkin emas, profilaktikajarayonida !")
        return MAIN_MENU


def food_menu(update, context):
    update.message.reply_text(
        "Menyulardan birini tanlang: ",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Lavashlar 🌯", "Burgerlar 🍔"],
                ['Shashliklar 🍡', 'Sushilar 🍣'],
                ['⬅️ Orqaga'],
            ],
            resize_keyboard=True
        )
    )
    return FOOD_MENU


def food_menu_select(update, context):
    text = update.message.text

    if text == "Lavashlar 🌯":
        update.message.reply_text("Lavash bor bu yerda")

    elif text == "Burgerlar 🍔":
        update.message.reply_text("Burgerlar bor bu yerda")

    elif text == "Shashliklar 🍡":
        update.message.reply_text("Shashliklar bor bu yerda")

    elif text == "Sushilar 🍣":
        update.message.reply_text("Sushilar bor bu yerda")

    elif text == "⬅️ Orqaga":
        main_menu(update, context)


def settings_menu(update, context):
    update.message.reply_text("Ma'lumotlarni tahrirlash: ",
                              reply_markup=ReplyKeyboardMarkup(
                                  [
                                      ["✏️ Ism familya"],
                                      ['📞 Telefon raqam'],
                                      ['⬅️ Orqaga'],
                                  ],
                                  resize_keyboard=True
                              ))
    return SETTINGS_MENU


def settings_select(update, context):
    text = update.message.text

    if text == "✏️ Ism familya":
        update.message.reply_text("✏️ Yangi ism familyani kiriting: ")
        return EDIT_NAME

    elif text == "📞 Telefon raqam":
        update.message.reply_text("📞 Yangi raqamingini kiriting: ", reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Raqamni yuborish", request_contact=True)]],
            resize_keyboard=True
        ))
        return EDIR_PHONE

    elif text == "⬅️ Orqaga":
        return main_menu(update, context)


def edit_name(update, context):
    db.update_name(update.effective_user.id, update.message.text)
    update.message.reply_text("Ism Familya muvofaqiyatli o'zgartirildi ✅")
    return main_menu(update, context)


def edit_phone(update, context):
    db.update_phone(update.effective_user.id, update.message.contact.phone_number)
    update.message.reply_text("Telefon raqam muvofaqiyatli o'zgartirildi ✅")
    return main_menu(update, context)


def main():
    db.crate_table()

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text, get_name)],
            PHONE: [MessageHandler(Filters.contact, get_phone)],
            LOCATION: [MessageHandler(Filters.location, get_location)],

            MAIN_MENU: [MessageHandler(Filters.text, main_menu_select)],
            SETTINGS_MENU: [MessageHandler(Filters.text, settings_select)],
            FOOD_MENU: [MessageHandler(Filters.text, food_menu_select)],

            EDIT_NAME: [MessageHandler(Filters.text, edit_name)],
            EDIR_PHONE: [MessageHandler(Filters.contact, edit_phone)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
