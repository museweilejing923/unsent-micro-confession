"""Unsent micro-confession writer.

Writes one fixed two-part text to /output/entry.txt: a "To:" line
naming the person, then the message that was never sent. The output
never changes: no arguments, no clock, no network, no randomness.
"""

import os
import string
import sys

LETTER = "To: Dad\nI still keep the voicemail where you said you were proud of me. I listen to it on bad days and have never told you."
TOTAL_LIMIT = 260
BODY_LIMIT = 200
ENDERS = ".!?"


def die(why):
    print("invalid: " + why, file=sys.stderr)
    raise SystemExit(1)


def body_has_lowercase(body):
    """True when the message holds at least one lowercase letter.

    A message typed entirely in capitals reads as shouting, not
    as something whispered and never sent, so it is refused.
    """
    for mark in body:
        if mark.islower():
            return True
    return False


def check_confession(text):
    if text.strip() == "":
        die("the confession is empty")
    halves = text.split("\n")
    if len(halves) != 2 or not halves[0].startswith("To: "):
        die("need exactly a To: line plus one message")
    address, body = halves
    if len(address) <= 4:
        die("the To: line names nobody")
    if len(text) > TOTAL_LIMIT:
        die("the confession is over 260 characters")
    if len(body) > BODY_LIMIT or body.strip() == "":
        die("the message is empty or over 200 characters")
    if any(ord(mark) == 127 or (ord(mark) < 32 and mark != "\n") for mark in text):
        die("the confession holds a control character")
    if body[-1] not in ENDERS:
        die("the message lacks closing punctuation")
    if all(mark in string.punctuation for mark in body):
        die("the message is only punctuation")
    if body.isdigit():
        die("the message is only digits")
    if not any(mark.isalpha() for mark in body):
        die("the message has no letters")
    if not body_has_lowercase(body):
        die("the message has no lowercase letters")


def run():
    check_confession(LETTER)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(LETTER + "\n")


if __name__ == "__main__":
    run()
