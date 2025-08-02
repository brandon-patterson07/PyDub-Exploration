# -*- coding: utf-8 -*-
"""
Created on Thu May  1 13:22:12 2025

@author: burkez, pattersonb
"""
import os
from pydub import AudioSegment
from pydub.effects import low_pass_filter, compress_dynamic_range
# --- Voice Effect Functions ---

def change_pitch(segment, octaves):
  """
  Changes the pitch of an AudioSegment.
  Args:
    segment: The input pydub AudioSegment.
    octaves: The number of octaves to shift the pitch by (can be fractional).
             Positive values raise the pitch, negative values lower it.
  Returns:
    A new AudioSegment with the pitch changed.
  """
  # Calculate the new frame rate based on the octave shift.
  # Shifting up an octave doubles the frequency (frame rate).
  # Shifting down an octave halves the frequency.
  # Formula: new_rate = old_rate * (2 ** octaves)
  new_sample_rate = int(segment.frame_rate * (2.0 ** octaves))
  # Keep the same samples but change the frame rate interpretation
  # This effectively changes pitch and speed. Pydub doesn't have
  # a built-in pitch shift independent of speed without external libraries/complex methods.
  return segment._spawn(segment.raw_data, overrides={'frame_rate': new_sample_rate})

def slow_down(segment, speed_factor):
    """
    Slows down an AudioSegment by a given factor.
    Args:
        segment: The input pydub AudioSegment.
        speed_factor: The factor by which to slow down (e.g., 0.95 for 95% speed).
                      Must be less than 1.0.
    Returns:
        A new AudioSegment slowed down.
    """
    if speed_factor >= 1.0:
        print("Warning: speed_factor for slow_down should be less than 1.0. Returning original segment.")
        return segment
    # To slow down, decrease the frame rate
    new_sample_rate = int(segment.frame_rate * speed_factor)
    return segment._spawn(segment.raw_data, overrides={'frame_rate': new_sample_rate})

def high_pitch_voice(segment):
  """Applies a high-pitch effect."""
  print("Applying high pitch effect...")
  # Increase pitch by 0.7 octaves (adjust as needed)
  return change_pitch(segment, 0.7)

def low_pitch_voice(segment):
  """Applies a low-pitch effect."""
  print("Applying low pitch effect...")
  # Decrease pitch by 0.5 octaves (adjust as needed)
  return change_pitch(segment, -0.5)

def robot_voice(segment):
  """Applies a simple 'robot' effect (pitch shift + slight speed up)."""
  print("Applying robot effect...")
  # Pydub doesn't have a vocoder. This is a simplified effect.
  # Increase pitch slightly
  pitched = change_pitch(segment, 0.3)
  # Speed up slightly (10%) - this also raises pitch further
  # Note: Pydub's speedup doesn't preserve pitch by default.
  sped_up = pitched.speedup(playback_speed=1.1)
  return sped_up

def echo_effect(segment, delay_ms=200, decay=0.8):
  """Adds an echo effect."""
  print(f"Applying echo effect (delay: {delay_ms}ms, decay: {decay})...")
  output = segment
  # Create delayed segments and overlay them with decay
  for i in range(1, 4): # Add 3 echoes
      delay = delay_ms * i
      # Create silence to prepend
      silence_segment = AudioSegment.silent(duration=delay)
      # Create the delayed version (shifted right)
      delayed_segment = silence_segment + segment
      # Reduce volume of the echo based on decay
      echo_volume = - (1 - decay**i) * 60 # Approximate dB reduction
      faded_echo = delayed_segment.apply_gain(echo_volume)
      # Overlay the echo onto the output
      output = output.overlay(faded_echo)
  return output

def whisper_voice(segment):
  """Applies a simulated 'whisper' effect (quieter, slightly faster)."""
  print("Applying whisper effect...")
  # Reduce volume significantly
  quieter = segment - 15 # Decrease volume by 15 dB
  # Speed up slightly (5%) - might make it sound a bit breathier/faster
  sped_up = quieter.speedup(playback_speed=1.05)
  return sped_up

#following voices were created by us
def yell_voice(segment):
  """Applies a simulated 'yell' effect (louder, slightly slower)."""
  print("Applying yell effect...")
  # Increase volume significantly
  louder = segment + 8 # Decrease volume by 8 dB
  # Slow down slightly (5%) - might make it sound a bit breathier/faster
  slowed_down = slow_down(louder, .95)
  return slowed_down

def turtle_voice(segment):
    """Applies a simulated 'turtle' effect (significantly slower)"""
    print("Applying turtle effect...")
    # Slow down significantly (50%) - makes the audio very slow and low-pitched
    slowed_down = slow_down(segment, .5)
    return slowed_down

def rabbit_voice(segment):
    """Applies a simulated 'rabbit' effect (significantly faster)"""
    print("Applying rabbit effect...")
    # Speed up significantly (75%) - makes the audio very fast and high-pitched
    segment = segment.speedup(playback_speed = 1.75)
    return segment

def reverse_voice(segment):
    """Reverses the audio"""
    print("Appying reverse effect...")
    return segment.reverse()

def underwater_voice(segment):
    print("Applying underwater effect...")
    filtered = low_pass_filter(segment, 500) #caps frequencies at 500hz
    compressed = compress_dynamic_range(filtered) #compresses audio
    quieter = compressed - 5
    sfx = AudioSegment.from_file("C:/Users/pattersonb/project/underwater_sfx.wav")
    combined = quieter.overlay(sfx)

    return combined
# --- Main Program Logic ---

def main():
  """Main function to run the voice changer."""
  print("--- Pydub Voice Changer ---")

  # 1. Get Input File
  while True:
    input_file = input("Enter the path to the input WAV file: ")
    if os.path.exists(input_file) and input_file.lower().endswith('.wav'):
      try:
        print(f"Loading '{input_file}'...")
        audio = AudioSegment.from_wav(input_file)
        print("File loaded successfully.")
        break
      except Exception as e:
        print(f"Error loading WAV file: {e}")
        print("Please ensure ffmpeg is installed and the file is a valid WAV.")
    else:
      print("Invalid path or file is not a .wav file. Please try again.")

  # 2. Choose Effect
  print("\nChoose a voice effect:")
  print("1: High Pitch")
  print("2: Low Pitch")
  print("3: Robot Voice (Simplified)")
  print("4: Echo Effect")
  print("5: Whisper Voice (Simulated)")
  print("6: Yell Voice(Simulated)")
  print("7: Turtle Voice")
  print("8: Rabbit Voice")
  print("9: Reverse Voice")
  print("10: Underwater Voice")

  while True:
    choice = input("Enter the number of the effect (1-10): ")
    if choice.isdigit() and 1 <= int(choice) <= 10:
      effect_choice = int(choice)
      break
    else:
      print("Invalid choice. Please enter a number between 1 and 9.")

  # 3. Apply Effect
  modified_audio = None
  if effect_choice == 1:
    modified_audio = high_pitch_voice(audio)
  elif effect_choice == 2:
    modified_audio = low_pitch_voice(audio)
  elif effect_choice == 3:
    modified_audio = robot_voice(audio)
  elif effect_choice == 4:
    modified_audio = echo_effect(audio)
  elif effect_choice == 5:
    modified_audio = whisper_voice(audio)
    #effect choices below were written by us
  elif effect_choice == 6:
      modified_audio = yell_voice(audio)
  elif effect_choice == 7:
      modified_audio = turtle_voice(audio)
  elif effect_choice == 8:
      modified_audio == rabbit_voice(audio)
  elif effect_choice == 9:
      modified_audio = reverse_voice(audio)
  elif effect_choice == 10:
      modified_audio = underwater_voice(audio)

  # 4. Get Output File Path
  while True:
      output_file = input("Enter the desired path for the output WAV file: ")
      if output_file.lower().endswith('.wav'):
          # Basic check to prevent overwriting input immediately
          if os.path.abspath(output_file.lower()) == os.path.abspath(input_file.lower()):
              print("Output file cannot be the same as the input file.")
          else:
              break
      else:
          print("Output file must end with .wav")


  # 5. Export Modified Audio
  try:
    print(f"Exporting modified audio to '{output_file}'...")
    modified_audio.export(output_file, format="wav")
    print("Export complete!")

  except Exception as e:
    print(f"Error exporting file: {e}")
    print("Please ensure you have write permissions and ffmpeg is installed correctly.")

if __name__ == "__main__":
  main()

