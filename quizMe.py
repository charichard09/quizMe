#Write program that reads file "read_to_dict.txt" consisting of questions and answers to dictionaries
#Date: 5-25-21 Developer: Richard Cha

import sys, os, re

def quiz_me():
    #os.path.dirname(sys.argv[0]) will return a string of readFileToDictionaryTest.py's directory path, which we assume read_to_dict.txt is also in
    read_to_dict_fo = open(os.path.dirname(sys.argv[0]) + "/quizQuestions.txt", 'r')

    read_to_dict_text = read_to_dict_fo.read()

    read_to_dict_fo.close()

    #Create a regular expression to look for all current "Questions on x" and print to screen. 
    print("\nCurrent Glossary of Available Questions:")
    available_questions_regex = re.compile(r"Questions\son\s.*")
    available_questions_mo = available_questions_regex.findall(read_to_dict_text)
    print('\n'.join(available_questions_mo))

    #Ask user input of what they'd like to be quizzed on from the options given.
    while True:
        user_topic = input("\nWhat would you like to be quizzed on today? (CH1, Universal Python, etc.)\n")
        if "Questions on " + user_topic in read_to_dict_text:
            break

    # Create a regular expression to isolate text inbetween string "Questions on {topic}" and "Questions on {following topic}"
    # Error: Quizzing on topic "X" is not stopping at the correct spot. Should be stopping at "Questions on Y"
    # FIXED 11-17-21: Reason was because compiling ".*" in .*Questions\son was being "greedy" and searching ALL
    # of the string until it could no longer find more "Questions\son". Fixed by limiting .* with .*? making .* match as
    # few characters as possible "Questions on" to ".*?!END"
    # Other solution was to make the end of each Questions On unique (i.e. "!END CH2")
    # 8-28-22: Add ability to have answers with newline characters for better readability and multiple answers.
    # Problem 8-28-22: On line 39 ...r"!A\.\s.*\n\n?", re.DOTALL) was still being greedy and assigning all answers to 
    # answers_match[0] instead of answer in first question to answers_match[0] and so on
    # Solution 8-29-222: With more understanding of the use of '?' special character and its use in "spam?"
    # and "*?" in regular expressions, the regular expression ...r"!A\.\s.*\n\n?", re.DOTALL) was allowing .* to ignore
    # all \n characters with no ? limiter thus greedily including everything until the final \n\n?
    # By moving the ? after * we limit the regex to find only the first instance of !A\.\s.*?\n\n
       
    quest_ans_regex = re.compile(r"Questions\son\s" + user_topic + r".*?!END", re.DOTALL)
    quest_ans_mo = quest_ans_regex.search(read_to_dict_text)

    #Assign all !Q. to a dictionary as keys with respective !A. as values
    questions_regex = re.compile(r"!Q\.\s.*")
    answers_regex = re.compile(r"!A\.\s.*?\n\n", re.DOTALL)

    questions_match = questions_regex.findall(quest_ans_mo.group())
    answers_match = answers_regex.findall(quest_ans_mo.group())

    quest_ans_dict = {}

    for i in range(len(questions_match)):
        quest_ans_dict[questions_match[i]] = answers_match[i]

    #Ask a random question from quest_ans_dict (random key), let user input their answer, then print the answer (value) of question (key)
    for j in range(len(quest_ans_dict)):
        user_answer = input('\n' + list(quest_ans_dict.keys())[j] + "\n\n")
        print('\n' + quest_ans_dict[list(quest_ans_dict.keys())[j]])

    #Exit prompt to user
    print("\nThat's all the questions. Great job!")

#Add option to be quizzed again
while True:
    quiz_me()
    answer = input("Would you like to be quizzed again, or on another topic? (y/n)\n")
    if answer == 'y':
        continue
    elif answer == 'n':
        break
    else:
        print("     ERROR: invalid input")
        break