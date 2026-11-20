#!/usr/bin/env python3
"""A terminal quiz game that loads questions from a JSON file."""

import argparse
import json
import random
from pathlib import Path

QUESTIONS_FILE = Path(__file__).resolve().parent / "questions.json"
HIGH_SCORE_FILE = Path(__file__).resolve().parent / "highscore.txt"


def load_questions(path=None):
    """Load a list of question dictionaries from a JSON file."""
    path = Path(path) if path else QUESTIONS_FILE
    with path.open(encoding="utf-8") as handle:
        questions = json.load(handle)

    for index, item in enumerate(questions, start=1):
        if "question" not in item or "options" not in item or "answer" not in item:
            raise ValueError(f"Question {index} is missing a required field.")
        if not 0 <= item["answer"] < len(item["options"]):
            raise ValueError(f"Question {index} has an invalid answer index.")
    return questions


def load_high_score(path=None):
    """Return the saved high score, or 0 if none has been recorded yet."""
    path = Path(path) if path else HIGH_SCORE_FILE
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8").strip()
    try:
        return max(0, int(text))
    except ValueError:
        return 0


def save_high_score(score, path=None):
    """Write a new high score to disk."""
    path = Path(path) if path else HIGH_SCORE_FILE
    path.write_text(str(int(score)) + "\n", encoding="utf-8")


def ask_question(item, get_input=input):
    """Print one multiple-choice question and return True if the answer is right."""
    print(f"\n{item['question']}")
    for index, option in enumerate(item["options"], start=1):
        print(f"  {index}. {option}")

    while True:
        raw = get_input("Your answer (1-{}): ".format(len(item["options"]))).strip()
        try:
            choice = int(raw)
        except ValueError:
            print("Please enter a number.")
            continue
        if 1 <= choice <= len(item["options"]):
            break
        print("That number is not one of the options. Try again.")

    correct = choice - 1 == item["answer"]
    if correct:
        print("Correct!")
    else:
        actual = item["options"][item["answer"]]
        print(f"Not quite. The correct answer is: {actual}")
    return correct


def play(questions, get_input=input, high_score_path=None):
    """Run a full quiz round and update the high-score file if needed."""
    high_score = load_high_score(high_score_path)
    print("Welcome to the terminal quiz!")
    print(f"There are {len(questions)} questions. Current high score: {high_score}")

    score = 0
    for item in questions:
        if ask_question(item, get_input=get_input):
            score += 1

    print(f"\nYou scored {score} out of {len(questions)}.")
    if score > high_score:
        save_high_score(score, high_score_path)
        print("New high score! Nice work.")
    elif score == high_score and score > 0:
        print("You tied the high score.")
    else:
        print(f"The high score is still {high_score}.")
    return score


def build_parser():
    parser = argparse.ArgumentParser(description="Play a short multiple-choice quiz in the terminal.")
    parser.add_argument(
        "-q",
        "--questions",
        default=str(QUESTIONS_FILE),
        help="Path to a JSON file of questions",
    )
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Keep the questions in file order instead of shuffling them",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    questions = load_questions(args.questions)
    if not args.no_shuffle:
        # Shuffle a copy so the JSON file stays in the original order.
        questions = questions[:]
        random.shuffle(questions)
    play(questions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
