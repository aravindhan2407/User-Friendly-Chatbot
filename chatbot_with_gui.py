import common, science, travel, food, gaming
from tkinter import *
from tkinter import font
from google_answer import *
from random import randrange
import pyttsx3

fo, tr, sc, ga, t = food.food, travel.travel, science.science, gaming.gaming, common.common_words
topicSelected, querySelected = False, True
results = []
query, topic = "", ""

def updateFile(name, dic):
    f = open(name+".py", "w")
    f.write(name+" = {\n")
    c = 0
    for key in dic:
      if c: f.write(",\n")
      else: c = 1  
      f.write("    "+"\""+key+"\" : \""+dic[key]+"\"") 
    f.write("\n}") 

def simplify(word):
    for symbol in common.symbols:
      word = word.replace(symbol,"")
    return word.lower() 

def speak(msg):
    speaker = pyttsx3.init()
    speaker.say(msg)
    speaker.runAndWait()

def sendResponse(msg):
    start = chatWindow.index(INSERT)
    chatWindow.config(state=NORMAL)
    chatWindow.insert(END,msg+"\n")
    chatWindow.tag_add("botmsg",start,INSERT)
    chatWindow.tag_config("botmsg",foreground="green")
    chatWindow.config(state=DISABLED)
    msgBox.delete("1.0",END)
    chatWindow.see(END)
    root.after(1, lambda: speak(msg))

def exitProgram():
    global fo, tr, sc, ga
    updateFile("food", fo) 
    updateFile("travel", tr)
    updateFile("science", sc)
    updateFile("gaming", ga)
    sendResponse("\n"+common.exitWords[randrange(0,len(common.exitWords))]+"\n")
    root.after(1000, lambda: exit())

def selectTopic(top):
    global t, topic
    if int(top) == 1: t, topic = fo, "food"
    elif int(top) == 2: t, topic = tr, "travel"
    elif int(top) == 3: t, topic = sc, "science"
    elif int(top) == 4: t, topic = ga, "gaming"    
    else: exitProgram()
    if int(top) in range(1,5): sendResponse("You have selected "+topic.title()+" section\nAsk your queries\n")

def searchGoogle():
    sendResponse(get_google_answer(query, my_api_key, my_cse_id))

def selectQuery(qno):
    qno = int(qno)
    if qno:
        global topic, results, query
        sendResponse("\n"+t[results[qno-1]]+"\n")
        if topic == "food": fo[query] = t[results[qno-1]]
        elif topic == "travel": tr[query] = t[results[qno-1]]
        elif topic == "science": sc[query] = t[results[qno-1]]
        elif topic == "gaming": ga[query] = t[results[qno-1]]
    else:
        searchGoogle()

def getResponse():
    global query, results, querySelected
    if query in t.keys():
        sendResponse("\n"+t[query]+"\n")
    else:
        s = simplify(query)
        m = False
        st = ""
        for key in t:
          if simplify(key) == s: 
            st = key
            m = True
            break
        if m:
          sendResponse("\n"+t[st]+"\n\nNext Query: \n")
          return
        s = query.lower().split()   
        for word in common.common_words:
          if word.lower() in s: s.remove(word)
        results = []   
        c = 0
        ma = 0
        for q in t:
          st = q.lower().split()
          c = 0
          for word in s:
            if word in st: 
              c+=1
          if c>ma: 
            results.clear()
            results.append(q)
            ma = c 
          elif c == ma:
            results.append(q)    
        if len(results) == 1:
          sendResponse("\n"+t[results[0]]+"\n")    
        elif len(results):     
          for i in range(len(results)):
            sendResponse("{}] {}".format(i+1,results[i]))
          sendResponse("\nWhich of the above questions are you expecting anwers for? (0 if there is no match)")
          querySelected = False
          return
        else:
          searchGoogle()
    sendResponse("\n\nNext Query: \n")

def sendMessage():
    global topicSelected, querySelected, msgBox, query
    msg = msgBox.get("1.0",END)
    start = chatWindow.index(INSERT)
    chatWindow.config(state=NORMAL)
    chatWindow.insert(END,msg+"\n")
    chatWindow.tag_add("mymsg",start,INSERT)
    chatWindow.tag_config("mymsg",foreground="red")
    chatWindow.config(state=DISABLED)
    msgBox.delete("1.0",END)
    chatWindow.see(END)
    if not topicSelected:
      topicSelected = True
      selectTopic(msg)
    elif not querySelected:
      querySelected = True
      selectQuery(msg)
    elif msg.replace("\n","").lower() == "exit":
      topicSelected = False
      sendResponse("\nSelect one of the following topics:\n1]Food\n2]Travel\n3]Science & Technology\n4]Gaming\nELSE Exit\n")
    else:
      query = msg.replace("\n","")
      getResponse()  

root = Tk()
root.title("Chatbot")
root.geometry("520x500")
root.resizable(width=FALSE, height=FALSE)

chatWindow = Text(root, bd=1, width="50", height="8", font=("Courier New", 13))
chatWindow.place(x=5,y=5, height=400, width=500)
start = chatWindow.index(INSERT)
chatWindow.insert(END,"\tWelcome to the chatbot\n")
chatWindow.tag_add("title",start,INSERT)
chatWindow.tag_config("title",font=font.Font(weight="bold"))
start = chatWindow.index(INSERT)
chatWindow.insert(END,"\nSelect one of the following topics:\n1]Food\n2]Travel\n3]Science & Technology\n4]Gaming\nELSE Exit\n\n")
chatWindow.tag_add("botmsg",start,INSERT)
chatWindow.tag_config("botmsg",foreground="green")
chatWindow.config(state=DISABLED)

msgBox = Text(root, bd=0,width="30", height="4", font=("Courier New", 17), background="lightgrey")
msgBox.place(x=5, y=410, height=40, width=430)

sendButton= Button(root, text="Send",  width="10", height=5,bd=0, bg="#0080ff", 
                activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12), command= lambda: sendMessage())
sendButton.place(x=440, y=410, height=40, width=65)

scrollbar = Scrollbar(root, command=chatWindow.yview)
scrollbar.place(x=505,y=5, height=385)

root.mainloop()