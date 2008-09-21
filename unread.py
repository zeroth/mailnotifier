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
def logout():
    mailbox.logout()

        
if __name__ == '__main__':
    try:
        login(sys.argv[1],sys.argv[2])
    except:
        print "Login Problem : Please try the correct user name and password"
    check_unread()
    logout()
    

    

