# Secret Santa

A small script to organize secret santa events.

The script assigns pairs and also sends out E-mails, informing the
participants, who they will be the secret santa of.

The participants information is provided to the script via a CSV file that
stores the participants full names (lowercase) in the first column and their
email addresses in the second column.

```csv
name, email
first-name last-name, first-name.last-name@email.com
...
```

The E-mails are sent via a local SMTP server which requires `SendMail`.

```{bash}
sudo apt install sendmail
```

The message can be provided by an template where `$secret_santa` will be
replaced by the first name of the receiver of the email, while `$receiver` will
be the full name of the person, that receives the gift.

```{bash}
python secret_santa.py --help
```

The list of participants is shuffled, and grouped into pairs. This leads to one monocyclic graph and no self-assignments.
Without the `--send` flag, no emails will be sent.

```{bash}
python secret_santa.py participants.csv --send
```
