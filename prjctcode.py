from neuralintents import GenericAssistant
import speech_recognition as sr 
import pyttsx3 as tts
import sys
import pyaudio

recognizer= sr.Recognizer()

speaker= tts.init()
speaker.setProperty('rate', 150)

todolist= ["finish python project", "go to school", "play guitar"]


def create_todo():
	global recognizer

	speaker.say("what do you want to write onto your note?")
	speaker.runAndWait()

	done= False

	while not done:
		try:
			with sr.Microphone() as mic:
				recognizer.adjust_for_ambient_noise(mic, duration= 0.2)
				audio= recognizer.listen(mic)

				note= recognizer.recognize_google(audio)
				note= note.lower()

				speaker.say("choose a filename")
				speaker.runAndWait()

				recognizer.adjust_for_ambient_noise(mic, duration= 0.2)
				audio= recognizer.listen(mic)

				filename= recognizer.recognize_google(audio)
				filename= filename.lower()

			with open(filename, 'w') as f:
				f.write(note)
				done= True
				speaker.say(f" {filename} note has been created")
				speaker.runAndWait()

		except :#sr.UnKnownValueError:
			recognizer= sr.Recognizer()
			speaker.say("i did not understand, please try again")
			speaker.runAndWait()


def add_todo():
	global recognizer

	speaker.say("do you want to add a task to your to do list?")
	speaker.runAndWait()

	done= False

	while not done:
		try:
			with sr.Microphone() as mic:
				recognizer.adjust_for_ambient_noise(mic, duration= 0.2)
				audio= recognizer.listen(mic)

				item= recognizer.recognize_google(audio)
				item= item.lower()
				
				todolist.append(item)
				done= True

				speaker.say(f"{item} added sucessfully")
				speaker.runAndWait()
		
		except :#sr.UnKnownValueError:
			recognizer= sr.Recognizer()
			speaker.say("i did not understand, please try again!")
			speaker.runAndWait()


def show_todo():

	speaker.say("you have the following on your to do list")
	
	for item in todolist:
		speaker.say(item)
		speaker.runAndWait()


#def check_todo():
	#checks if the item in completed then return a response via speaker

def hello():

	speaker.say("hello, waiting for your order sir")
	speaker.runAndWait()


def quit():
	
	speaker.say("farewell sir")
	speaker.runAndWait()
	sys.exit(0)


mapping= {
	
	"greeting": hello,
	"create_note": create_todo,
	"add_todo": add_todo,
	"show_todo": show_todo,
	#"check_todo": check_todo,
	"exit": quit
}	

assistant= GenericAssistant('myintents.json',intent_methods= mapping)
assistant.train_model()
#assistant.save_model()

while True:
	try:
		with sr.Microphone() as mic:
			recognizer.adjust_for_ambient_noise(mic, duration= 0.2)
			audio= recognizer.listen(mic)

			message= recognizer.recognize_google(audio)
			message= message.lower()

			assistant.request(message)
	
	except :#sr.UnKnownValueError:
		recognizer= sr.Recognizer()
			