"""
Email Filter
Author: Aaron Ducote
"""

import csv
import re


def filter_emails(letter):
    """
    filter_emails: filters emails to take out incorrect addresses
    :param letter: letter of emails to be filtered
    """

    output_file = 'csrankings-' + letter + '_emails_filtered.csv'

    csv_file = csv.reader(open('csrankings-' + letter + '_emails.csv', "r"), delimiter=",")

    email_list = []
    row_num = 0
    emails = []

    for row in csv_file:
        bad = 0     # resets bad to 0 (good) with each new row
        row_num += 1
        if row_num % 2 == 0:        # skips the even empty rows
            continue

        # bad_list : common phrases or characters in invalid email addresses caught by crawler
        bad_list = ['subject', 'Subject', 'spam', '%', '[', '<', ':', 'SPAM', 'SUBJECT', 'dot', '(', '/', ')', '(', 'firstname']
        for i in bad_list:
            if i in row[1]:
                bad = 1     # email is invalid and input as bad
                print('Bad Email found: ' + row[1])
                break
        if bad == 1:        # checks if something in the bad list was found in the email address (invalid)
            continue
        if row[1] == 'email found':     # filler title
            continue
        if row[1] == '':    # empty email
            print('Bad Email found: ' + row[1])
            continue
        row[1] = str(row[1])    # converted to string for functionality
        for e in emails:
            if e == row[1]:     # if duplicate of documented email
                bad = 1         # email is bad and should not be used again
                print('Bad Email found: Duplicate ' + row[1])
                break
        if '@' not in row[1]:
            bad = 1
        if bad == 1:        # checks if email is bad and should be skipped
            continue
        emails.append(row[1])       # add to emails list to check for duplicates
        email_list.append([row[0], filter_non_ascii(row[1])])    # add name and email to list

    with open(output_file, 'w', newline='') as file:        # write names and emails to csv
        writer = csv.writer(file)
        writer.writerows(email_list)

    # print(email_list)


def filter_non_ascii(input_str):
    return re.sub(r'[^\x00-\x7F]+', '', input_str)


if __name__ == "__main__":
    filter_emails('m')    # Enter letter you want to filter
    print('open csrankings-letter_emails_filtered.csv for filtered results')

