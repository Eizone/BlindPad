import os
import wave
import pyaudio
import subprocess
from array import array
from pydub import AudioSegment
import time

#Module to convert the Wav file to speech
def get_record_audio():
	os.system("python ./sttClient.py -credentials 9f4b5a3f-b552-46dc-80ad-7e2ffb819ad9:z6AapDecdLJR -model en-US_BroadbandModel -threads 10")
	fp = open("./output/hypotheses.txt","r")
	B = fp.readline()
	B = B[3:]
	return B

#Module to create a wav file by recording
def record_audio():
	THRES = 30000
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = 6
	WAVE_OUTPUT_FILENAME = "./recordings/rec.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	os.system('espeak -v en-us -s 120 "You may speak"')
	print "* Recording audio..."
	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		as_ints = array('h', data)
		max_value = max(as_ints)
		if max_value > THRES:
			frames.append(data)

	print "* done\n" 

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	wf = wave.open(WAVE_OUTPUT_FILENAME,'r')
	if os.stat(WAVE_OUTPUT_FILENAME).st_size != 0:
		filter(WAVE_OUTPUT_FILENAME)
	
def filter(WAVE_OUTPUT_FILENAME):
	song = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
	new = song.low_pass_filter(15000)
	new.export(out_f=WAVE_OUTPUT_FILENAME, format="wav")

#Module to check for the keyword
def check(A):
	options = ['yeah','stop','right','next']
	for i in range(len(options)):
		if A.find(options[i])!= -1:
			return i+1
	return 0

#Module to Confirm the keyword
def confirm(n):
	if(n==1):
		os.system('espeak -v en-us -s 120 "Did you mean begin?"')
	elif(n==2):
		os.system('espeak -v en-us -s 120 "Did you mean stop?"')
	elif(n==3):
		os.system('espeak -v en-us -s 120 "Did you mean note?"')
	elif(n==4):
		os.system('espeak -v en-us -s 120 "Did you mean next?"')
	record_audio()
	rec=get_record_audio()
	if rec.find('yes')!=-1 :
		return n
	elif rec.find('this')!=-1 :
		return n
	else:
		return -1

#Module to choose file
def filemodule():
	fp = open("./Files/file1.txt","r")
	return fp

n=0
run = 1
fp = filemodule()
fc = open("./Notes/file1.txt","wb")
while(run):
	#choose file module
	record_audio()
	A = get_record_audio()
	n = check(A)
	if n!=0:
		c = confirm(n)
		if c!=-1:
			if c==1:
				#if 
				B = fp.readline()
				query = ['espeak','-v','en-us','-s','120',B]
				subprocess.call(query)
				#else:
				#	os.system('espeak -v en-us -s 120 "File Empty!"')
			elif c==2:
				fp.close()
				B = "The process has been terminated"
				query = ['espeak','-v','en-us','-s','120',B]
				subprocess.call(query)
				run = 0
			elif c==3:
				fc.write(B)
				B = "Note taken"
				query = ['espeak','-v','en-us','-s','120',B]
				subprocess.call(query)
			elif c==4:
				#if 
				B = fp.next()
				query = ['espeak','-v','en-us','-s','120',B]
				subprocess.call(query)
				#else:
				#	os.system('espeak -v en-us -s 120 "End Of File!"')
