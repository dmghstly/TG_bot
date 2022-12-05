import telebot
import telebot.types as types
import emoji
import translators as tss
import time
import random

# need to implement rock paper cissors
# need to implement the game dice
bot = telebot.TeleBot("5801656587:AAFQ52gnwIL-n2ey1N3Ny9Jl4VC0qDajex4")
rps_dict = {1: ":rock:", 2: ":scroll:", 3: ":scissors:"}
dice_dict = {1: "\u2680", 2: "\u2681", 3: "\u2682",
             4: "\u2683", 5: "\u2684", 6: "\u2685"}


def solve_rps(player, comp):
    match player:
        case 1:
            if comp == 1:
                return "draw"
            elif comp == 2:
                return "lose"
            elif comp == 3:
                return "win"

        case 2:
            if comp == 1:
                return "win"
            elif comp == 2:
                return "draw"
            elif comp == 3:
                return "lose"

        case 3:
            if comp == 1:
                return "lose"
            elif comp == 2:
                return "win"
            elif comp == 3:
                return "draw"


def play_dice(user_id):
    bot.send_message(user_id, "3...")
    time.sleep(0.5)
    bot.send_message(user_id, "2...")
    time.sleep(0.5)
    bot.send_message(user_id, "1...")
    time.sleep(0.5)

    pl_num1 = random.randint(1, 6)
    pl_num2 = random.randint(1, 6)

    bot.send_message(user_id,
                     emoji.emojize("You've got: " + dice_dict[pl_num1] + " and " + dice_dict[pl_num2], language='alias'))
    time.sleep(0.5)
    bot.send_message(user_id, "Your score: " + str(pl_num1 + pl_num2))
    time.sleep(0.5)

    bot.send_message(user_id, "3...")
    time.sleep(0.5)
    bot.send_message(user_id, "2...")
    time.sleep(0.5)
    bot.send_message(user_id, "1...")
    time.sleep(0.5)

    comp_num1 = random.randint(1, 6)
    comp_num2 = random.randint(1, 6)

    bot.send_message(user_id,
                     emoji.emojize("Computer've got: " + dice_dict[comp_num1] + " and " + dice_dict[comp_num2],
                                   language='alias'))
    time.sleep(0.5)
    bot.send_message(user_id, "Computer score: " + str(comp_num1 + comp_num2))
    time.sleep(0.5)

    if pl_num1 + pl_num2 > comp_num1 + comp_num2:
        bot.send_message(user_id, "Look's like you've won")
    elif pl_num1 + pl_num2 < comp_num1 + comp_num2:
        bot.send_message(user_id, "Sorry, you've lost")
    elif pl_num1 + pl_num2 == comp_num1 + comp_num2:
        bot.send_message(user_id, "Wow, you've got a draw")


def play_rps(user_id, option):
    bot.send_message(user_id, "Rock...")
    time.sleep(0.5)
    bot.send_message(user_id, "Paper...")
    time.sleep(0.5)
    bot.send_message(user_id, "Scissors...")
    time.sleep(0.5)

    op_move = random.randint(1, 3)

    result = solve_rps(option, op_move)

    bot.send_message(user_id, emoji.emojize('You: ' + rps_dict[option] + ' vs ' + 'Comp: ' + rps_dict[op_move],
                                            language='alias'))

    match result:
        case "win":
            bot.send_message(user_id, "Congrats!!! You've won!")
        case "lose":
            bot.send_message(user_id, "Oops, you've lost")
        case "draw":
            bot.send_message(user_id, "Guess nobody won")


def initiate_rps(user_id):
    keyboard = types.InlineKeyboardMarkup()

    key_rock = types.InlineKeyboardButton(text=emoji.emojize(':rock:', language='alias'),
                                          callback_data=str(user_id) + ":rock")
    keyboard.add(key_rock)

    key_paper = types.InlineKeyboardButton(text=emoji.emojize(':scroll:', language='alias'),
                                           callback_data=str(user_id) + ":paper")
    keyboard.add(key_paper)

    key_scissors = types.InlineKeyboardButton(text=emoji.emojize(':scissors:', language='alias'),
                                              callback_data=str(user_id) + ":scissors")
    keyboard.add(key_scissors)

    bot.send_message(user_id, text='Choose your move:', reply_markup=keyboard)


def translate_to_en(user_id, text):
    try:
        translation = tss.google(text)
        bot.send_message(user_id, "Translation: " + translation)

    except:
        bot.send_message(user_id, "Sorry, I can't translate it. Try again.")


def initiate_actions(user_id):
    keyboard = types.InlineKeyboardMarkup()

    key_rps = types.InlineKeyboardButton(text='Rock paper scissors', callback_data=str(user_id) + ":rps")
    keyboard.add(key_rps)

    key_dice = types.InlineKeyboardButton(text='Play some dice', callback_data=str(user_id) + ":dice")
    keyboard.add(key_dice)

    bot.send_message(user_id, text='Choose option', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user = message.from_user

    if message.text == "Hello":
        bot.send_message(user.id, "Привет, {}".format(str(user.username)))
    elif message.text == "/help":
        bot.send_message(user.id, "This bot has a few functions: \n \n"
                                  "1. If you want to be greeted type: Hello \n \n"
                                  "2. If you want to check some commands type: /actions \n \n"
                                  "3. /actions has some games.\n \n"
                                  "4. If you want to translate something to english \n"
                                  "type /translate:(and some text).\n \n"
                                  "Good luck using bot and have a great time.")
    elif message.text == "/actions":
        initiate_actions(user.id)

    elif message.text.startswith("/translate"):
        translate_to_en(user.id, message.text[11:len(message.text)])

    else:
        bot.send_message(user.id, "Sorry, did not get you. Try typing /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data = call.data

    params = data.split(":")

    match params[1]:
        case "rps":
            initiate_rps(int(params[0]))
        case "rock":
            play_rps(int(params[0]), 1)
        case "paper":
            play_rps(int(params[0]), 2)
        case "scissors":
            play_rps(int(params[0]), 3)
        case "dice":
            play_dice(int(params[0]))


bot.polling(none_stop=True, interval=0)
