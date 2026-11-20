import json
from pathlib import Path

import pytest

import quiz


SAMPLE_QUESTIONS = [
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5"],
        "answer": 1,
    },
    {
        "question": "Which language is this quiz written in?",
        "options": ["Java", "Python", "C++"],
        "answer": 1,
    },
]


@pytest.fixture
def questions_file(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(SAMPLE_QUESTIONS), encoding="utf-8")
    return path


def test_load_questions_reads_valid_json(questions_file):
    loaded = quiz.load_questions(questions_file)
    assert len(loaded) == 2
    assert loaded[0]["question"] == "What is 2 + 2?"


def test_load_questions_rejects_a_bad_answer_index(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(
        json.dumps([{"question": "Hi?", "options": ["A"], "answer": 5}]),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="invalid answer index"):
        quiz.load_questions(path)


def test_play_scores_answers_and_saves_a_high_score(tmp_path):
    high_score_path = tmp_path / "highscore.txt"
    answers = iter(["2", "2"])  # both answers are option 2, which is correct

    score = quiz.play(
        SAMPLE_QUESTIONS,
        get_input=lambda _prompt: next(answers),
        high_score_path=high_score_path,
    )

    assert score == 2
    assert quiz.load_high_score(high_score_path) == 2


def test_play_does_not_overwrite_a_better_high_score(tmp_path):
    high_score_path = tmp_path / "highscore.txt"
    quiz.save_high_score(10, high_score_path)
    answers = iter(["1", "1"])  # both wrong

    score = quiz.play(
        SAMPLE_QUESTIONS,
        get_input=lambda _prompt: next(answers),
        high_score_path=high_score_path,
    )

    assert score == 0
    assert quiz.load_high_score(high_score_path) == 10
