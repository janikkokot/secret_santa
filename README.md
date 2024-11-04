# Secret Santa

A small script to organize secret santa events.

The script assigns pairs and also sends out E-mails, informing the
participants, who they will be the secret santa of.

The participants information is provided to the script via a CSV file that
stores the participants full names (lowercase) in the first column and their
email adresses in the second column. The E-mails are sent via a local smtp server.

```{bash}
sudo apt install sendmail
```

The message can be provided by an template where `$secret_santa` will be
replaced by the first name of the receiver of the email, while `$receiver` will
be the full name of the person, that receives the gift.

The program will exit without sending emails if any person has been assigned
themselves. In these cases, just re-execute the script. In the future, the
assigning process could be updated to be more sophisticated, which would
resolve this issue.
