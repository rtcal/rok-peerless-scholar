import json
import re

from spellchecker import SpellChecker


def jaccard_similarity(question, user_input):
    set1 = set(question.split())
    set2 = set(user_input.split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union


def prepare_user_input(user_input: str) -> str:
    user_input = user_input.strip().lower()
    user_input = re.sub(r'[^a-zA-Z0-9 ]+', '', user_input).strip()

    spell = SpellChecker()
    words = user_input.split()
    corrected_words = [spell.correction(word) for word in words]
    user_input = ' '.join([i for i in corrected_words if i])

    return user_input


def find_closest_match(user_input: str, question_data) -> dict:
    user_input = prepare_user_input(user_input)

    closest_similarity = 0
    closest_question = None

    for qa in question_data:
        similarity = jaccard_similarity(qa['question'], user_input)

        if similarity > closest_similarity:
            closest_question = qa
            closest_similarity = similarity

    return closest_question


def main():
    with open("data.json", "r") as f:
        question_data = json.load(f)

    if not question_data:
        print("Question data not found! Stopping...")

    while True:
        user_input = input("Question prompt: ")

        if user_input in ["quit", "q", "exit"]:
            print("Exiting...")
            break

        qa = find_closest_match(user_input, question_data)

        if not qa:
            print("No information found!")
            continue

        print("----- ----- ----- ----- -----")
        print(f"QUESTION: {qa['question']}")
        print(f"ANSWER: {qa['answer']}")
        print("----- ----- ----- ----- -----")


if __name__ == '__main__':
    main()
