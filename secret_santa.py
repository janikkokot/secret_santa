#! /usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime
from email.message import EmailMessage
import logging
import random
from smtplib import SMTP
import textwrap
from typing import NamedTuple, NewType, TypeVar, Iterator


T = TypeVar('T')
Email = NewType('Email', str)


class Participant(NamedTuple):
    name: str
    adress: Email
    
    @property
    def firstname(self):
        return ' '.join(self.name.split()[:-1])


def create_pairs(participants: list[T]) -> list[tuple[T, T]]:
    """Every Participant will be assigned another random Participant."""
    santas = participants
    receivers = participants.copy()
    random.shuffle(receivers)

    for i, (santa, receiver) in enumerate(zip(santas, receivers[:-1])):
        if santa == receiver:
            receivers[i], receivers[i+1] = receivers[i+1], receivers[i]

    return list(zip(santas, receivers))



def create_message(santa: Participant, receiver: Participant) -> EmailMessage:
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
        logging.warning('-'*80)
        logging.warning(f'{santa.name:<32} is the same as {receiver.name:>32}')
        raise ValueError('The santa and receiver should be two different participants')

    msg = EmailMessage()
    msg['Subject'] = 'TCI Secret Santa'
    msg['From'] = 'secret_santa@uibk.ac.at'
    msg['To'] = santa.adress
    msg.set_content(textwrap.dedent(content))

    logging.info(f'{santa.name:<33} was assigned {receiver.name:>33}')
    return msg


def get_participants(filename: str) -> list[Participant]:
    """Read in participants from a csv file."""
    participants = []
    with open(filename) as csv:
        for line in csv:
            name, email = line.split(',')
            _part = Participant(
                        name.strip(),
                        Email(email.strip()),
                        )
            participants.append(_part)
    return participants


def main(filename):
    participants = get_participants(filename)
    pairs = create_pairs(participants)
    try:
        msgs = [create_message(santa, receiver) for santa, receiver in pairs]
    except ValueError:
        logging.warning('No messages have been sent, try again.')
        logging.debug(pairs)
        raise ValueError('No messages have been sent, try again.') from None
#     with SMTP('smtp.uibk.ac.at') as connection:
#         for msg in msgs:
#             connection.send_message(msg)


if __name__ == '__main__':
    # logging setup
    logging.basicConfig(filename='secret_santa.log',
                        format='%(message)s',
                        level=logging.DEBUG,
                        )
    logging.info(f'{f"{datetime.now():%d/%m/%y %H:%M}":=^80}')
    # parser setup
    parser = argparse.ArgumentParser(
            prog='Secret Santa',
            description='Assign each participant a secret santa',
            epilog='Frohe Weihnachten!',
            )
    parser.add_argument('adress_file', help="File that contains entries of the form 'full name, email adress' for each participant.")

    args = parser.parse_args()
    for a, v in vars(args).items():
        logging.info(f'{a}: {v}')
    main(args.adress_file)
