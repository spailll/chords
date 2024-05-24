from tkinter import Canvas, Button, Tk
import pygame
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Initialize the Pygame mixer
pygame.mixer.init()

# Function to generate a sine wave for a given frequency
def generate_sine_wave(frequency, duration, sample_rate=44100):
    # Generate a sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    signal = np.sin(frequency * 2 * np.pi * t)
    return signal

# Function to play a note of a given frequency
def play_note(frequency, duration=1.0):
    signal = generate_sine_wave(frequency, duration)
    sound = pygame.sndarray.make_sound((signal * 32767).astype(np.int16))
    sound.play()

# Function to visualize waveform and FFT
def visualize(frequencies, duration=1.0):
    sample_rate = 44100
    combined_wave = np.sum([generate_sine_wave(f, duration, sample_rate) for f in frequencies], axis=0)
    
    # Plot the waveform
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(combined_wave[:2000])
    plt.title("Waveform")

    # Plot the FFT
    yf = fft(combined_wave)
    xf = np.linspace(0.0, sample_rate/2.0, len(yf) // 2)
    plt.subplot(2, 1, 2)
    plt.plot(xf, 2.0/len(combined_wave) * np.abs(yf[:len(combined_wave) // 2]))
    plt.title("FFT")
    plt.show()

# Function to handle a key press
def on_key_press(event, key):
    if key not in pressed_keys:
        print(f"Key {key} pressed")
        pressed_keys.add(key)
    else:
        print(f"Key {key} released")
        pressed_keys.remove(key)
    play_note_sequence()
     

# Function to handle a key release
# def on_key_release(key):
#     if key in pressed_keys:
#         print(f"Key {key} released")
#         pressed_keys.remove(key)
#         play_note_sequence()

# Function to play the current sequence of notes
def play_note_sequence():
    if pressed_keys:
        frequencies = [key_to_frequency[i] for i in pressed_keys]
        visualize(frequencies)
        play_chord(frequencies)

def play_chord(frequencies):
    duration = 1.0
    sample_rate = 44100
    combined_wave = np.sum([generate_sine_wave(f, duration, sample_rate) for f in frequencies], axis=0)
    sound = pygame.sndarray.make_sound((combined_wave * 32767).astype(np.int16))
    sound.play()

# Piano key frequencies(A0 - C8)
key_to_frequency = {
                    'C0': 16.35, 'C#0': 17.32, 'D0': 18.35, 'D#0': 19.45, 'E0': 20.60,'F0': 21.83, 'F#0': 23.12, 'G0': 24.50, 'G#0': 25.96, 'A0': 27.50,'A#0': 29.14, 'B0': 30.87,
                    'C1': 32.70, 'C#1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'E1': 41.20,'F1': 43.65, 'F#1': 46.25, 'G1': 49.00, 'G#1': 51.91, 'A1': 55.00,'A#1': 58.27, 'B1': 61.74,
                    'C2': 65.41, 'C#2': 69.30, 'D2': 73.42, 'D#2': 77.78, 'E2': 82.41,'F2': 87.31, 'F#2': 92.50, 'G2': 98.00, 'G#2': 103.83, 'A2': 110.00,'A#2': 116.54, 'B2': 123.47,
                    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81,'F3': 174.61, 'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'A3': 220.00,'A#3': 233.08, 'B3': 246.94,
                    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63,'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00,'A#4': 466.16, 'B4': 493.88,
                    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25,'F5': 698.46, 'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.00,'A#5': 932.33, 'B5': 987.77,
                    'C6': 1046.50, 'C#6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'E6': 1318.51,'F6': 1396.91, 'F#6': 1479.98, 'G6': 1567.98, 'G#6': 1661.22, 'A6': 1760.00,'A#6': 1864.66, 'B6': 1975.53,
                    'C7': 2093.00, 'C#7': 2217.46, 'D7': 2349.32, 'D#7': 2489.02, 'E7': 2637.02,'F7': 2793.83, 'F#7': 2959.96, 'G7': 3135.96, 'G#7': 3322.44, 'A7': 3520.00,'A#7': 3729.31, 'B7': 3951.07,
                    'C8': 4186.01, 'C#8': 4434.92, 'D8': 4698.64, 'D#8': 4978.03, 'E8': 5274.04,'F8': 5587.65, 'F#8': 5919.91, 'G8': 6271.93, 'G#8': 6644.88, 'A8': 7040.00,'A#8': 7458.62, 'B8': 7902.13
                   }

pressed_keys = set()

# GUI setup
root = Tk()
root.title("Virtual Piano")
canvas = Canvas(root, width=2520, height=500)
canvas.pack()

white_keys = ['C0', 'D0', 'E0', 'F0', 'G0', 'A0', 'B0',
              'C1', 'D1', 'E1', 'F1', 'G1', 'A1', 'B1',
              'C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2',
              'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3',
              'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
              'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
              'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
              'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
              'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8',
             ]
black_keys = ['C#0', 'D#0', 'F#0', 'G#0', 'A#0',
              'C#1', 'D#1', 'F#1', 'G#1', 'A#1',
              'C#2', 'D#2', 'F#2', 'G#2', 'A#2',
              'C#3', 'D#3', 'F#3', 'G#3', 'A#3',
              'C#4', 'D#4', 'F#4', 'G#4', 'A#4',
              'C#5', 'D#5', 'F#5', 'G#5', 'A#5',
              'C#6', 'D#6', 'F#6', 'G#6', 'A#6',
              'C#7', 'D#7', 'F#7', 'G#7', 'A#7',
              'C#8', 'D#8', 'F#8', 'G#8', 'A#8',
             ]
black_ke_positions = [0,1,3,4,5]

key_width = 40
key_height = 200
black_key_width = 25
black_key_height = 120

# Create piano keys
for j, key in enumerate(white_keys):
    key_id = canvas.create_rectangle(j * key_width, 0,j * key_width + key_width, key_height, fill="white")
    canvas.addtag_withtag(key, key_id)
    canvas.tag_bind(key, '<ButtonPress-1>', lambda e, k=key: on_key_press(e, k))
    # canvas.tag_bind(key, '<ButtonRelease-1>', lambda e, k=key: on_key_release(e, k))

black_key_index = 0
for j in range(len(white_keys)):
    if j % 7 in black_ke_positions:
        key = black_keys[black_key_index]
        key_id = canvas.create_rectangle(j * key_width + 3/4 * key_width, 0,j * key_width + 3/4 * key_width + black_key_width, black_key_height, fill="black")
        canvas.addtag_withtag(key, key_id)
        canvas.tag_bind(key, '<ButtonPress-1>', lambda e, k=key: on_key_press(e, k))
        # canvas.tag_bind(key, '<ButtonRelease-1>', lambda e, k=key: on_key_release(e, k))
        black_key_index += 1
root.mainloop()




