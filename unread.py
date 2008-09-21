#!/usr/bin/env python
# unread is the command line tool to check unread mail via IMAP.
# we are using imaplib to access a imap email.
# 
# Copyright (C) 2008  Abhishek Patil <abhishek@thezeroth.net>.
#
# unread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# unread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unread.  If not, see <http://www.gnu.org/licenses/>.



import imaplib, sys

#time being we are using gmail imap server 
SERVER = 'imap.gmail.com'
PORT = 993
mailbox = imaplib.IMAP4_SSL(SERVER,PORT)

def login(user, password):
    """
    This function login to the user account using give username and password.
    by command line.
    """
    print mailbox.login(user,password)

def check_unread():
    """
    This function select INBOX as a default folder and check of the unread mails 
    and displays the number of unread emails are available.
    """
    print mailbox.select()
    if len(mailbox.search(None,"UNSEEN")[1]) >= 1:
        print mailbox.search(None,"UNSEEN")[1]
        print "there is/are %d email/s" % len(mailbox.search(None,"UNSEEN")[1][0].split())
    else:
        print " there are no UNREAD Messagees"
    return mailbox.search(None,"UNSEEN")[1]

def fetch_mail(mail_uid):
    """
    This function reads each unread mails and displays
    FROM TO CC DATE & SUBJECT of the each unread mail.
    """
    for uid in mail_uid[0].split():
        typ, data = mailbox.fetch(uid,'(BODY[HEADER.FIELDS (FROM TO CC DATE SUBJECT)])')
        sub = data[0][1].strip()
        sub = sub.replace('\r\n','\n')
        print sub, '\n'

def logout():
    """
    This function logout from the session.
    """
    mailbox.logout()

        
if __name__ == '__main__':
    """
    TODO: impliment the command line parser getopt.
    """
    try:
        login(sys.argv[1],sys.argv[2])
    except:
        print "Login Problem : Please try the correct user name and password"
    fetch_mail(check_unread())
    logout()
    

    

