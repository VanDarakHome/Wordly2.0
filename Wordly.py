import random


def load_words(name):
    with open(name, 'r', encoding='utf-8') as file:
        word_list = file.read().splitlines()
    return [word for word in word_list if '-' not in word and ' ' not in word]


def choose_word(word_list, min_len, max_len):
    return random.choice([word for word in word_list if min_len <= len(word) <= max_len])


def compare_words(hidden, guess, correct_pos):
    new_cor_pos = correct_pos.copy()
    correct_letters = set()
    for i in range(len(hidden)):
        if hidden[i] == guess[i]:
            new_cor_pos[i] = hidden[i]
        elif guess[i] in hidden:
            correct_letters.add(guess[i])
    return new_cor_pos, correct_letters


def display_word(hidden, correct_pos):
    display_list = []
    for i in range(len(hidden)):
        if correct_pos[i]:
            display_list.append(correct_pos[i])
        else:
            display_list.append('_')
    return ' '.join(display_list)


def display_keyboard(not_used_letters, language):
    if language == 'russian':
        keyboard = [
            'й ц у к е н г ш щ з х ъ',
            'ф ы в а п р о л д ж э',
            'я ч с м и т ь б ю'
        ]
        not_used_letters_phrase = "Буквы, которые не использовались:"
    else:
        keyboard = [
            'q w e r t y u i o p',
            'a s d f g h j k l',
            'z x c v b n m'
        ]
        not_used_letters_phrase = "Letters, that don't used:"

    print(f"\n{not_used_letters_phrase}")
    for row in keyboard:
        row_now = []
        for letter in row.split():
            if letter in not_used_letters:
                row_now.append(' ')
            else:
                row_now.append(letter)
        print(' '.join(row_now))
    print()


def select_language():
    print("Выберите язык игры / Select game language:")
    print("1. Русский")
    print("2. English")
    choice = input("Введите номер / Enter the number: ")
    return 'russian' if choice == '1' else 'english'


def select_difficulty(language):
    if language == 'russian':
        length_limit_for_custom = 30
        phrases = {
            "difficulty": "Выберите уровень сложности:",
            "easy": "Легкий (слова до 7 букв, 8 попыток)",
            "medium": "Средний (слова 7-12 букв, 6 попыток)",
            "hard": "Сложный (слова 12-16 букв, 6 попыток)",
            "custom": "Кастомный",
            "min_length": "Введите минимальную длину слова: ",
            "max_length": "Введите максимальную длину слова: ",
            "attempts": "Введите количество попыток: ",
            "invalid_length": "Длина слова должна быть не более 30 букв.",
            "invalid_attempts": "Количество попыток должно быть положительным."
        }
    else:
        length_limit_for_custom = 18
        phrases = {
            "difficulty": "Select difficulty level:",
            "easy": "Easy (words up to 7 letters, 8 attempts)",
            "medium": "Medium (words 7-12 letters, 6 attempts)",
            "hard": "Hard (words 12-16 letters, 6 attempts)",
            "custom": "Custom",
            "min_length": "Enter minimum word length: ",
            "max_length": "Enter maximum word length: ",
            "attempts": "Enter number of attempts: ",
            "invalid_length": "Word length must not exceed 18 letters.",
            "invalid_attempts": "Number of attempts must be positive."
        }

    print(phrases["difficulty"])
    print("1. " + phrases["easy"])
    print("2. " + phrases["medium"])
    print("3. " + phrases["hard"])
    print("4. " + phrases["custom"])
    choice = input("Введите номер: ")
    
    if choice == '1':
        return 0, 7, 8
    elif choice == '2':
        return 7, 12, 6
    elif choice == '3':
        return 12, 16, 6
    elif choice == '4':
        while True:
            min_len = int(input(phrases["min_length"]))
            max_len = int(input(phrases["max_length"]))
            if max_len > length_limit_for_custom:
                print(phrases["invalid_length"])
            elif max_len < min_len:
                print("Максимальная длина должна быть больше или равна минимальной.")
            else:
                break
        while True:
            attempts = int(input(phrases["attempts"]))
            if attempts <= 0:
                print(phrases["invalid_attempts"])
            else:
                break
        return min_len, max_len, attempts
    else:
        print("Неправильный выбор. Пожалуйста, выберите заново.")
        return select_difficulty(language)


language = select_language()
if language == 'russian':
    word_list = load_words('russian.dict')
    phrases = {
        "word_length": "Угадайте слово из {} букв.",
        "enter_word": "Введите слово: ",
        "word_length_error": "Слово должно быть длиной {} букв.",
        "win": "Поздравляем! Вы угадали слово.",
        "current_state": "Текущее состояние: {}",
        "letters_in_word": "Буквы в слове, но не на своих местах: {}",
        "attempts_left": "Осталось попыток: {}",
        "lose": "Вы проиграли. Загаданное слово было: {}",
        "play_again": "Хотите сыграть еще раз? (да/нет): ",
        "invalid_choice": "Пожалуйста, введите 'да' или 'нет'.",
        "guessed_letters": "Вы угадали следующие буквы: {}"
    }
else:
    word_list = load_words('english.dict')
    phrases = {
        "word_length": "Guess a word with {} letters.",
        "enter_word": "Enter the word: ",
        "word_length_error": "The word must be {} letters long.",
        "win": "Congratulations! You guessed the word.",
        "current_state": "Current state: {}",
        "letters_in_word": "Letters in the word but not in the correct positions: {}",
        "attempts_left": "Attempts left: {}",
        "lose": "You lost. The word was: {}",
        "play_again": "Do you want to play again? (yes/no): ",
        "invalid_choice": "Please enter 'yes' or 'no'.",
        "guessed_letters": "You guessed the following letters: {}"
    }

while True:
    min_len, max_len, attempts = select_difficulty(language)
    hidden_word = choose_word(word_list, min_len, max_len)
    correct_pos = [None] * len(hidden_word)
    used_letters = set()
    guessed_in_word = set()

    print(phrases["word_length"].format(len(hidden_word)))

    while attempts > 0:
        guess = input(phrases["enter_word"]).lower()
        if len(guess) != len(hidden_word):
            print(phrases["word_length_error"].format(len(hidden_word)))
            continue

        if guess == hidden_word:
            print(phrases["win"])
            break

        used_letters.update(set(guess))
        correct_pos, letters = compare_words(hidden_word, guess, correct_pos)
        guessed_in_word.update(letters)
        display_list = display_word(hidden_word, correct_pos)
        print(phrases["current_state"].format(display_list))
        print(phrases["letters_in_word"].format(', '.join(letters)))
        print(phrases["guessed_letters"].format(', '.join(sorted(guessed_in_word))))

        display_keyboard(used_letters, language)

        attempts -= 1
        print(phrases["attempts_left"].format(attempts))

    if attempts == 0:
        print(phrases["lose"].format(hidden_word))

    restarting = input(phrases["play_again"]).lower()
    if restarting in ['да', 'yes']:
        continue
    elif restarting in ['нет', 'no']:
        print("Спасибо за игру! / Thank you for playing!")
        break
    else:
        print(phrases["invalid_choice"])
