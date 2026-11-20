# Terminal Quiz

A short multiple-choice quiz you can play in the terminal. Questions are stored in a JSON file, and the game keeps a high score in `highscore.txt`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The game itself only needs the Python standard library. Install the requirements if you want to run the tests.

## Usage

```bash
python quiz.py
```

You will see a question and numbered options. Type the number of your answer and press Enter.

Example:

```
Welcome to the terminal quiz!
There are 10 questions. Current high score: 0

What is the chemical symbol for water?
  1. H2O
  2. O2
  3. CO2
  4. NaCl
Your answer (1-4): 1
Correct!

...

You scored 8 out of 10.
New high score! Nice work.
```

Keep the questions in file order (no shuffling):

```bash
python quiz.py --no-shuffle
```

Use your own question file:

```bash
python quiz.py -q my_questions.json
```

Each question in the JSON file looks like this:

```json
{
  "question": "What is 2 + 2?",
  "options": ["3", "4", "5"],
  "answer": 1
}
```

The `answer` field is a zero-based index into the `options` list, so `1` means the second option.

## Tests

```bash
pytest
```
