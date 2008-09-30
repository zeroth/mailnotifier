#!/usr/bin/env python
# email-notifier is the command line tool to check unread mail via IMAP.
# I am using imaplib to access email via imap.
#
# Copyright (C) 2008  Abhishek Patil <abhishek@thezeroth.net>.
#
# email-notifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# email-notifier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unread.  If not, see <http://www.gnu.org/licenses/>.



import imaplib, sys, ConfigParser, getpass, os.path, getopt

mailbox =""

def login(user, password,ssl,server,port):
    """
    This function login to the user account using give username and password.
    by command line.
    """
    global mailbox
#    print user, password, ssl, server, port
    if ssl:
        mailbox = imaplib.IMAP4_SSL(host = server, port = port)
        
    else:
        mailbox = imaplib.IMAP4(host = server, port = port)

    try:
        mailbox.login(user,password)
    except:
        print "Error in Login Please Try correct username & password or check your Internet connection"
        sys.exit(1)

def check_unread():
    """
    This function select INBOX as a default folder and check of the unread mails
    and displays the number of unread emails are available.
    """
    global mailbox

    mailbox.select()
    if len(mailbox.search(None,"UNSEEN")[1]) >= 1:
        mailbox.search(None,"UNSEEN")[1]
        print "there is/are %d email/s" % len(mailbox.search(None,"UNSEEN")[1][0].split())
    else:
        print " there are no UNREAD Messages"
    return mailbox.search(None,"UNSEEN")[1]

def fetch_mail(mail_uid):
    """
    This function reads each unread mails and displays
    FROM TO CC DATE & SUBJECT of the each unread mail.
    """
    global mailbox

    for uid in mail_uid[0].split():
        typ, data = mailbox.fetch(uid,'(BODY[HEADER.FIELDS (FROM TO CC DATE SUBJECT)])')
        sub = data[0][1].strip()
        sub = sub.replace('\r\n','\n')
        print sub, '\n'

def logout():
    """
    This function logout from the session.
    """
    global mailbox
    mailbox.logout()
    

def manual_login():
    """
    when useing maual mode user have to send a user name as commandline argument
    with option -m <username>
    """
    config = ConfigParser.ConfigParser()
    notifier_file = os.path.join(os.getcwd(), os.path.dirname(__file__)) + "notifier_manual.conf" #gives the current path
    config.read(notifier_file)
    server = config.get('imap','server') #url for imap server eg. imap.gmail.com
    #print SERVER
    port = config.getint('imap','port') #Port number of imap server
    #print PORT
    ssl = config.getboolean('imap','ssl') # whether to use SSL encryption or not.
    #print SSL
    
    user = raw_input("Please Enter Your Username: ")
    psw = getpass.getpass("Please Enter Password: ")
    
    login(user,psw,ssl, server, port)
    fetch_mail(check_unread())
    logout()

def auto_login():
    """
    read the notifier_auto.conf file, config file format would be
    [<name/tag for the accout>]
    server = <imap server>
    port = <imap server port>
    ssl = <True/False> # use ssl incription or not
    userid = <username>
    password = <password>
    """
    config_auto = ConfigParser.ConfigParser()
    
    config_auto.read( os.path.join(os.getcwd(), os.path.dirname(__file__)) + "notifier_auto.conf")
    ac_list = config_auto.sections()
    total_ac = len(ac_list)
    
    for ac in ac_list:
        print ac
        userid = config_auto.get(ac,'userid')
        password = config_auto.get(ac,'password')
        ssl = config_auto.getboolean(ac,'ssl')
        server = config_auto.get(ac,'server')
        port = config_auto.getint(ac,'port')
        login(userid,password,ssl,server,port)
        fetch_mail(check_unread())
        logout()
        print"------------------------"
        
    
    
def argv_parser():
    decision =""
    options, remainder = getopt.getopt(sys.argv[1:],'m,a',['manual','auto'])
    for opt, arg in options:
        if opt in ('-a','--auto'):
            auto_login()
        elif opt in ('-m','--manual'):
            manual_login()

if __name__ == '__main__':
    """
    TODO: # use proper exception.
          # create a common function for  manual_login and auto_login to read conf file
    """
    argv_parser()

