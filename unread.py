#!/usr/bin/env python


import imaplib, sys

SERVER = 'imap.gmail.com'
PORT = 993
mailbox = imaplib.IMAP4_SSL(SERVER,PORT)
def login(user, password):
    print mailbox.login(user,password)

def check_unread():
    print mailbox.select()
    if len(mailbox.search(None,"UNSEEN")[1]) >= 1:
        print mailbox.search(None,"UNSEEN")[1]
        print "there is/are %d email/s" % len(mailbox.search(None,"UNSEEN")[1][0].split())
    else:
        print " there are no UNREAD Messagees"
    return mailbox.search(None,"UNSEEN")[1]
def fetch_mail(mail_uid):
    for uid in mail_uid[0].split():
        typ, data = mailbox.fetch(uid,'(BODY[HEADER.FIELDS (FROM TO CC DATE SUBJECT)])')
        sub = data[0][1].strip()
        sub = sub.replace('\r\n','\t')
        print sub

def logout():
    mailbox.logout()

        
if __name__ == '__main__':
    try:
        login(sys.argv[1],sys.argv[2])
    except:
        print "Login Problem : Please try the correct user name and password"
    fetch_mail(check_unread())
    logout()
    

    

