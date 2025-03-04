def ask_question(question,options,correct_answer):
    print(question)
    for option in options:
        print(option)
    user_ans=input("Enter the correct option number: ")
    return user_ans == correct_answer