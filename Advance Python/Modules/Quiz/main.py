from quiz_module import ask_question

questions=[
    ("What is the 2+2?",["1. 3","2. 4","3. 5","4. 6"],"2"),
    ("Which animal is known as the king of jungle?",["1. Lion","2. Elephant","3. Tiger","4. Bear"],"1"),
    ("What is the capital of India?",["1. Mumbai","2. Delhi","3. Pune","4. Nashik"],"2")
]

score = 0
for question,options,correct_answer in questions:
    if ask_question(question,options,correct_answer):
        score += 1

print(f"\nQuiz Completed!! \nYou have scored {score} out of {len(questions)}.")