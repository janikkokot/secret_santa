#! /usr/bin/env python3

from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime
from email.message import EmailMessage
import logging
import random
import csv
from smtplib import SMTP, SMTPException
from string import Template
from pathlib import Path
import textwrap
from typing import NamedTuple, NewType, TypeVar


T = TypeVar("T")
Email = NewType("Email", str)


class Participant(NamedTuple):
    name: str
    adress: Email

    @property
    def firstname(self):
        return " ".join(self.name.split()[:-1])


def create_pairs(participants: list[T]) -> list[tuple[T, T]]:
    """Every Participant will be assigned another random Participant."""
    random.shuffle(participants)
    receivers = deque(participants)
    receivers.rotate(-1)  # to the left
    return list(zip(participants, receivers))


def create_message(
    santa: Participant, receiver: Participant, message: Template
) -> EmailMessage:
    """Creates a Message object which can be sent through a SMPT session."""

    content = f"""\
    Dear {santa.firstname.title()},

    You have drawn {receiver.name.title()}.

    The present should not be more expensive than 20€.
    They will be unpacked together on Thursday at the TCI Christmas Party.

    Best,
    The Secret Santa Team
    """
    if santa == receiver:
        logging.warning("-" * 80)
        logging.warning(f"{santa.name:<32} is the same as {receiver.name:>32}")
        raise ValueError("The santa and receiver should be two different participants")

    content = textwrap.dedent(
        message.substitute(
            secret_santa=santa.firstname.title(),
            receiver=receiver.name.title(),
        )
    )

    msg = EmailMessage()
    msg["Subject"] = "TCI Secret Santa"
    msg["From"] = "secret_santa@uibk.ac.at"
    msg["To"] = santa.adress
    msg.set_content(content)

    logging.info(f"{santa.name:<33} was assigned {receiver.name:>33}")
    return msg


def get_participants(filename: str) -> list[Participant]:
    """Read in participants from a csv file."""
    participants = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            _part = Participant(name=row["name"], adress=Email(row["email"]))
            participants.append(_part)
    return participants


def main(filename: str, message_template: Template, send: bool = False):
    participants = get_participants(filename)
    pairs = create_pairs(participants)
    try:
        msgs = [
            create_message(santa, receiver, message_template)
            for santa, receiver in pairs
        ]
    except ValueError:
        logging.warning("No messages have been sent, try again.")
        logging.debug(pairs)
        raise ValueError("No messages have been sent, try again.") from None
    if send:
        logging.info("\nSending messages..")
        with SMTP("smtp.uibk.ac.at") as connection:
            for msg in msgs:
                try:
                    connection.send_message(msg)
                except SMTPException as err:
                    logging.error(f"Message could not be sent!\n{err}\n{msg}")
    else:
        logging.warning(
            "\nNo messages were sent! If this was not intended, use the '--send' flag!\n"
        )
        logging.info(f"This is an example message:\n{msgs[0].get_content()}")


if __name__ == "__main__":
    # logging setup
    logging.basicConfig(
        filename="secret_santa.log",
        format="%(message)s",
        level=logging.DEBUG,
    )
    # parser setup
    parser = argparse.ArgumentParser(
        prog="Secret Santa",
        description="Assign each participant a secret santa",
        epilog="Frohe Weihnachten!",
    )
    parser.add_argument(
        "adress_file",
        help="File that contains entries of the form 'full name, email adress' for each participant.",
    )
    parser.add_argument(
        "--template",
        help="Template of the message that will be sent to every participant",
        default=Path(__file__).parent / "MESSAGE_FROM_SANTA",
        type=Path,
    )
    parser.add_argument(
        "--send", action="store_true", help="Required to actually send the E-mails."
    )

    args = parser.parse_args()
    if not args.send:
        # if not send, print also to stderr
        logging.getLogger().addHandler(logging.StreamHandler())

    logging.info(f'{f"{datetime.now():%d/%m/%y %H:%M}":=^80}')
    for a, v in vars(args).items():
        logging.info(f"{a}: {v}")

    with open(args.template) as msg:
        message_template = Template(msg.read())
    logging.info(
        f'The message template is as follows:\n"""\n{textwrap.dedent(message_template.template)}"""\n'
    )

    main(args.adress_file, message_template, send=args.send)
    logging.info("Programm ran succesfully.")
