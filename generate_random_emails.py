#! /usr/bin/env python3

import random
import string
import argparse

def parse_input():
    parser = argparse.ArgumentParser(
            prog='Random Email Generator for Secret Santa',
            description='Generates a list of random names and email with each line containing "name, email"',
            )
    parser.add_argument('-n', help="Number of random names to generate", default=10, required=False)
    parser.add_argument('-out', help="Path of output file", default="./random_names_and_emails.txt", required=False)

    args = parser.parse_args()
    return args

def generate_random_name():
    first_names = ["John", "Jane", "David", "Emily", "Michael", "Sarah", "Chris", "Emma", "Alex", "Olivia", "Klaus", "Thomas", "Hubert"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Schmid","Mustermann","Musterfrau","Billa","Aldi"]
    return f"{random.choice(first_names)} {random.choice(string.ascii_uppercase)}. {random.choice(last_names)}"

def generate_random_email(name):
    domain = "@example.com"
    name = name.lower().replace('.','').replace(" ", ".") # John A. Deere -> john.a.deere
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return f"{name}{random_chars}{domain}"

def generate_random_data(num_entries):
    data = []
    for _ in range(num_entries):
        name = generate_random_name()
        email = generate_random_email(name)
        data.append(f"{name}, {email}")
    return data

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        for entry in data:
            file.write(entry + '\n')

if __name__ == "__main__":
    args = parse_input()
    generated_data = generate_random_data(args.n)
    save_to_file(generated_data, args.out)
    print(f"File '{args.out}' created with {args.n} random names and emails.")