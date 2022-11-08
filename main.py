import wave
from sys import argv
wave_r = wave.open(argv[1], 'rb') # whatever
wave_r_params = wave_r.getparams()
wave_w = wave.open("test.wav",'wb')
wave_w.setparams((wave_r_params.nchannels,wave_r_params.sampwidth,wave_r_params.framerate,wave_r_params.nframes,"NONE","NONE"))
# wave_w.setparams((1,1,wave_r_params.framerate,wave_r_params.nframes,"NONE","NONE"))
data = bytearray()
wave_r_frames_iterator = iter(wave_r.readframes(-1))
c = 0
try:
    while 1:
        # organization into seperate channels
        channels = []
        for channel in range(wave_r_params.nchannels):
            samples = []
            for sample in range(wave_r_params.sampwidth):
                nextframe = next(wave_r_frames_iterator)
                samples.append(nextframe)
                data.append(nextframe)
            channels.append(samples)
        print(c,channels)
        # conversion to (sampwidth=1,nchannels=1)
        #l = []
        #for channel in channels:
        #    l.append(channel[-1])
        #print(channels,end="-")
        # print(int(sum(l)/len(l)))
        # if int(sum(l)/len(l)) >= 128:
        #     data.append(int(sum(l)/len(l)) - 127)
        # if int(sum(l)/len(l)) <= 127:
        #     data.append(int(sum(l)/len(l)) + 128)
                # (sum([i<<(c*8) for c,i in enumerate(channel)]))
        #-----
        #to output what was inputted
        # ->
        #for channel in range(wave_r_params.nchannels):
        #    for byte in range(wave_r_params.sampwidth):
        #        n = next(wave_r_frames_iterator)
        #        data.append( n )
        #        print( n )
        c+=1
except Exception as e:
    print(e)
input("hit return to write")
print(data)
print(wave_r_params)
# wave_w.writeframes(b"\x00\xff")
wave_w.writeframes(data)
wave_w.close()
# ---------------------------------------------
r"""
# WAVE DATA FORMAT:
# Channels increase positively :
# ( When nchannels=2 (which it usually is),
#   then values would be in the order of
#   the left channel, then the right channel
#   )
# [Signed] Values are big endian :
# ( When sampwidth>=1, if value is 10203,
#   then it would be encoded as b"\xdb\x27"
#   )
# All of the data, when written into a file
# using wave.writeframes(), should produce the
# same sound (when played) using the given sampwidth
# and channel params on the right b string
# (This will produce the loudest possible click
# on device's given speakerset)
# - b"\x00\xff" when (sampwidth=1,channels=1)
# --- Straightforward; unsigned values. x00 is completely low, x7f is ~middle, xff is completely high.
# - b"\x00\x00\xff\xff" when (sampwidth=1,channels=2)
# --- \x00(Left channel @ frame 0), \x00(Right channel @ frame 0),
# --- \xff(Left channel @ frame 1), \xff(Right channel @ frame 1)
# - b"\x00\x80\x00\x7f" when (sampwidth=2,channels=1) : \x00\x80(@ frame 0) \x00\x7f(@ frame 1)
# --- \x00\x80(@ frame 0) \xff\x7f(@ frame 1)
# --- Why the weird numbers?: Values are signed (dont forget big endian.)
# ---   \xff\x7f is the highest positive number. \x00\x80 is the
# ---   lowest negative number. Both played after one-another, therefore click.
# - b"\x00\x80\x00\x80\xff\x7f\xff\x7f" when (sampwidth=2,channels=2)
# --- \x00\x80(Left channel @ frame 0), \x00\x80(Right channel @ frame 0),
# --- \xff\x7f(Left channel @ frame 1), \xff\x7f(Right channel @ frame 1)
"""