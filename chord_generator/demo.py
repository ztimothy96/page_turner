from scamp import *
import numpy as np

s = Session(tempo = 100) #tempo=100, default_soundfont
# s.print_default_soundfont_presets()
# default_spelling_policy: allows accidentals in a specified key
# just spelling: can put sharp or flats
# clock.set_tempo_target() can accel or rit.; set the transcription clock to the part clock...

# s.fast_forward_to_beat(100)
# Envelope objects: allow graduations such as cresc, dim


violin = s.new_part("Violin")
piano = s.new_part("Piano")
root = 69 # A 440

pitches = [0, 0, 7, 7, 9, 9, 7, 5, 5, 4, 4, 2, 2, 0]
durations = [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2]

maj = np.array([0, 4, 7])

def piano_part():
    piano.play_chord(root + maj, 1, 4)
    

def violin_part():
    for pitch, duration in zip(pitches, durations):
        violin.play_note(root + pitch, 1, duration) # can also specify staccato, vibrato, etc

s.start_transcribing()
s.fork(violin_part)
s.fork(piano_part)
s.wait_for_children_to_finish()


performance = s.stop_transcribing()
performance.to_score(title="Twinkle twinkle little star", composer="Anon").show()
# can specifiy barline locations, scamp will figure out the time signature :O
# show_xml() can open in another editor e.g. musescore
