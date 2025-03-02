import re

def load_dict(name):
    with open(name, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def get_masked_words(mask, dictionary):
    list_of_words = []
    word_len = len(mask)
    for word in dictionary:
        if len(word) != word_len:
            continue
        match = True
        for i in range(word_len):
            if mask[i] != '_' and mask[i] != word[i]:
                match = False
                break
        if match:
            list_of_words.append(word)
    return list_of_words

def filter_by_extra_letters(words, extra_letters):
    filtered_words = []
    for word in words:
        word_set = set(word)
        extra_set = set(extra_letters)
        if extra_set.issubset(word_set):
            filtered_words.append(word)
    return filtered_words

def main():
    print("Выберите язык / Choose language:")
    print("1. Русский / Russian")
    print("2. Английский / English")
    
    choice = input("Введите номер / Enter number: ")
    
    if choice == '1':
        dictionary = load_dict('russian.dict')
        lang = 'ru'
    elif choice == '2':
        dictionary = load_dict('english.dict')
        lang = 'en'
    else:
        print("Неправильный выбор / Incorrect choice.")
        return
    
    while True:
        if lang == 'ru':
            mask = input("Введите маску (например, а_то__з): ")
            extra_letters = input("Введите дополнительные буквы (без пробелов): ")
            result_text = "Список подходящих слов:"
            no_result_text = "Подходящих слов не найдено."
        else:
            mask = input("Enter mask (e.g., a_t_o__z): ")
            extra_letters = input("Enter additional letters (without spaces): ")
            result_text = "List of matching words:"
            no_result_text = "No matching words found."
        
        print(f"Дополнительные буквы: {extra_letters} / Additional letters: {extra_letters}")
        
        masked_words = get_masked_words(mask, dictionary)
        filtered_words = filter_by_extra_letters(masked_words, extra_letters)
        
        if filtered_words:
            print(result_text)
            for word in filtered_words:
                print(word)
        elif masked_words:
            print("Слова по маске найдены, но не содержат все дополнительные буквы.")
            print("Список слов по маске:")
            for word in masked_words:
                print(word)
        else:
            print(no_result_text)
        
        if lang == 'ru':
            check_again = input("Хотите проверить еще одно слово? (да/нет): ")
        else:
            check_again = input("Do you want to check another word? (yes/no): ")
        
        if check_again.lower() not in ['да', 'yes']:
            break

if __name__ == "__main__":
    main()
