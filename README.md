# TCI Secret Santa

A small script to organize the yearly TCI secret santa event.

The script assigns pairs and also sends out E-mails, informing the
participants, who they will be the secret santa of.

The participants information is provided to the script via a csv file that
stores the participants full names (lowercase) in the first column and their
email adresses in the second column. The E-mails are sent via the smtp server
of the university, which does not check for authentification, as long as the
script is run inside the universities network. This also allows to use the fake
email adress of `secret.santa@uibk.ac.at`.

The message can be provided by an template where `$secret_santa` will be
replaced by the first name of the receiver of the email, while `$receiver` will
be the full name of the person, that receives the gift.

The programm will exit without sending emails if any person has been assigned
themselves. In these cases, just reexecute the script. In the future, the
assigning process could be updated to be more sophisiticated, which would
resolve this issue.
