import re


phone_book = {}


def input_error(func):

    def inner(*args):

        try:

            return func(*args)
        
        except Exception as e:

            error = str(e)
            func_name = error.split(" ", 1)[0]
            func_name = func_name.removeprefix("cmd_").removesuffix("()").replace("_", " ")
            param_numbers = re.findall('\d+', error)

            # Example:
            # cmd_add() missing 1 required positional argument: 'number'
            # cmd_change() missing 2 required positional arguments: 'name' and 'number'
            if error.find("required positional argument") != -1:
                print(f"Missing {param_numbers[0]} required parameter{'s' if int(param_numbers[0]) > 1 else ''} "
                      f"for command '{func_name}'.") 
                              
                if func_name == "add" or func_name == "change":

                    if int(param_numbers[0]) == 1:
                        print(
                            f"Please enter phone number.\n"  
                            f"Correct syntax: {func_name} <username> <number>\n")   
                                             
                    elif int(param_numbers[0]) == 2:
                        print(
                            f"Please enter username and phone number.\n"  
                            f"Correct syntax: {func_name} <username> <number>\n")
                        
                elif func_name == "phone":
                    print(
                        f"Please enter username.\n"
                        f"Correct syntax: {func_name} <username>\n")  
                        
            # Example:
            # cmd_exit() takes 0 positional arguments but 1 was given
            # cmd_change() takes 2 positional arguments but 3 were given
            elif error.find("positional arguments but") != -1:
                print(
                    f"Incorrect number of parameters for command '{func_name}'.\n"
                    f"Must be {param_numbers[0]}, but {param_numbers[1]} {'were' if int(param_numbers[1]) > 1 else 'was'} given: {list(args)}\n")

    return inner


@input_error
def cmd_hello() -> str:

    result = "How can I help you?\n"
    
    return result


@input_error
def cmd_add(name: str, number: str) -> str:

    result = ""

    if phone_book.get(name, "") == "":
        phone_book[name] = number
        result = f"The user '{name}' has been successfully added to the phone book with number '{number}'\n"

    elif phone_book[name] == number:
        result = f"The entry '{name} - {number}' already exists in the phone book.\nNothing to add.\n"

    else:
        result = f"The user '{name}' already exists in the phone book with number '{phone_book[name]}'.\nTry 'change' command instead.\n"
    
    return result


@input_error
def cmd_change(name: str, number: str) -> str:

    result = ""

    if phone_book.get(name, "") == "":
        result = f"The user '{name}' does not exists in the phone book.\nTry 'add' command instead.\n"

    elif phone_book[name] == number:
        result = f"The entry '{name} - {number}' already exists in the phone book.\nNothing to change.\n"

    else:               
        phone_book[name] = number
        result = f"The user '{name}' has been successfully changed. New number is '{number}'.\n"

    return result


@input_error
def cmd_phone(name: str) -> str:

    result = ""

    if phone_book.get(name, "") == "":
        result = f"The user '{name}' does not exists in the phone book.\nTry 'add' command instead.\n"

    else:
        result = f"{name} - {phone_book[name]}\n"

    return result    


@input_error
def cmd_show_all() -> str:

    result = "Phone book:\n"

    for key, value in phone_book.items():
        result += f"{key} - {value}\n"

    return result


@input_error
def cmd_exit() -> str:

    result = "Good bye!\n"

    return result


@input_error
def cmd_help() -> str:

    result = ""

    for function in bot_functions:
        result += "{:<27}{:<}\n".format(function["help_name"],
                                        function["help_descr"])

    return result


def cmd_unknown(*_) -> str:

    result = "Unknown command. Please try again.\n"

    return result


def get_handler(cmd: str):

    for func in bot_functions:
        if (func["name"] == cmd) or (cmd in func.get("aliase", [])):
            return func["code"]
        
    else:
        return cmd_unknown


def prepare_handler(input_words: list) -> list:

    input_words_count = len(input_words)

    if input_words_count:
            
        if input_words_count >= 2:
            # For 'good bye' and 'show all' commands 
            if ((input_words[0] == "good" and input_words[1] == "bye") or
                (input_words[0] == "show" and input_words[1] == "all")):

                input_words[0] = " ".join([input_words[0], input_words.pop(1)])
                prepare_handler(input_words)

            # For input looks like this: 
            # add "Oleh Petrovych Davydenko aka Fks" 7846735987
            # add 'Oleh Petrovych Davydenko aka Fks' 7846735987
            else:
                for char in "\"'":
                    if (input_words_count > 2 and
                        input_words[1].startswith(char) and not input_words[1].endswith(char)):

                        current_word = ""
                        closing_quotes = False
                        closing_quotes_elem = 0

                        for i in range(2, input_words_count):
                            if input_words[i].startswith(char):
                                break

                            current_word = " ".join([current_word, input_words[i]])
                            closing_quotes_elem = i

                            if input_words[i].endswith(char):
                                closing_quotes = True
                                break

                        if closing_quotes:
                            input_words[1] = "".join([input_words[1], current_word])
                            input_words[1] = input_words[1].removeprefix(char).removesuffix(char)

                            while closing_quotes_elem >= 2:
                                input_words.pop(closing_quotes_elem)
                                closing_quotes_elem -= 1
    
    return input_words


bot_functions = [
    {
        "name": "hello",
        "code": cmd_hello,
        "help_name": "hello",
        "help_descr": "Бот відповідає у консоль \"How can I help you?\"."
    },
    {
        "name": "add",
        "code": cmd_add,
        "help_name": "add <username> <number>",
        "help_descr": "Бот зберігає новий контакт. !! Ім'я та номер телефону вводяться обов'язково через пробіл !!"
    },
    {
        "name": "change",
        "code": cmd_change,
        "help_name": "change <username> <number>",
        "help_descr": "Бот зберігає новий номер телефону існуючого контакту. !! Ім'я та номер телефону вводяться обов'язково через пробіл !!"
    },
    {
        "name": "phone",
        "code": cmd_phone,
        "help_name": "phone <username>",
        "help_descr": "Бот виводить у консоль номер телефону для зазначеного контакту."
    },
    {
        "name": "show all",
        "code": cmd_show_all,
        "help_name": "show all",
        "help_descr": "Бот виводить всі збереженні контакти з номерами телефонів у консоль."
    },
    {
        "name": "exit",
        "code": cmd_exit,
        "help_name": "exit (close, good bye)",
        "help_descr": "Бот завершує свою роботу.",
        "aliase": ["close", "good bye"]
    },
    {
        "name": "help",
        "code": cmd_help,
        "help_name": "help",
        "help_descr": "Бот відповідає у консоль цим повідомленням."
    },
]


def main():

    print("\nCLI Bot Assistant [Version 1.0]")
    print("Type help for help\n")

    while True:
        user_input = input(">> ")
        input_words = re.findall('\S+', user_input.lower())

        if (prepare_handler(input_words)):
            handler = get_handler(input_words.pop(0))
            result = handler(*input_words)
            if result:
                print(result)
                if result.find("Good bye!") != -1:
                    exit()


if __name__ == '__main__':
    main()
