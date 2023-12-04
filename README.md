# TCI Secret Santa

A small script to organize the yearly TCI secret santa event.

The script assigns pairs and also sends out E-mails, informing the
participants, who they will be the secret santa of.

The participants information is provided to the script via a csv file that
stores the user names in the first column and their email adresses in the
second column. The E-mails are sent via the smtp server of the university,
which does not check for authentification, as long as the script is run inside
the universities network. This also allows to use the fake email adress of
`secret.santa@uibk.ac.at`.

The message is currently hard-coded, but this could for future uses be updated
to also be provided in a small additional text file.
