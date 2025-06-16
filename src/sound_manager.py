import pygame
import os
import sys
from src.constants import DEFAULT_MUSIC_VOLUME, DEFAULT_SFX_VOLUME

# Try to import the resource_path function
try:
    from resource_path import resource_path
except ImportError:
    # If not available, define it here
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Set volume levels from constants
        self.music_volume = DEFAULT_MUSIC_VOLUME
        self.sfx_volume = DEFAULT_SFX_VOLUME
        self.muted = False
        
        # Dictionary to store sound effects
        self.sounds = {}
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all game sounds"""
        sound_path = resource_path(os.path.join('assets', 'sounds'))
        print(f"Looking for sound files in: {sound_path}")
        
        # Check if sound files exist and load them
        try:
            # Sound effects
            self._try_load_sound('jump', [
                os.path.join(sound_path, 'jump.wav'),
                os.path.join(sound_path, 'jump-audio.mp3'),
                os.path.join(sound_path, 'jump.mp3')
            ])
            
            self._try_load_sound('land', [
                os.path.join(sound_path, 'land.wav')
            ])
            
            self._try_load_sound('glitch', [
                os.path.join(sound_path, 'glitch.wav')
            ])
            
            self._try_load_sound('level_complete', [
                os.path.join(sound_path, 'level_complete.wav')
            ])
            
            # Game over sound (single death)
            self._try_load_sound('game_over', [
                os.path.join(sound_path, 'pixel-explosion-319166.mp3'),
                os.path.join(sound_path, 'game-over.mp3'),
                os.path.join(sound_path, 'death.mp3'),
                os.path.join(sound_path, 'death.wav')
            ])
            
            # Final death sound (when out of lives)
            self._try_load_sound('final_death', [
                os.path.join(sound_path, 'pixel-death-66829.mp3'),
                os.path.join(sound_path, 'final-death.mp3'),
                os.path.join(sound_path, 'final-death.wav')
            ])
            
            # Game completion sound
            self._try_load_sound('game_completed', [
                os.path.join(sound_path, 'goodresult-82807.mp3'),
                os.path.join(sound_path, 'complete.mp3'),
                os.path.join(sound_path, 'complete.wav')
            ])
            
            # Set volumes for all sounds
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
                
        except Exception as e:
            print(f"Error loading sounds: {e}")
            print("Continuing without sound effects.")
    
    def _try_load_sound(self, sound_name, file_paths):
        """Try to load a sound from multiple possible file paths"""
        for path in file_paths:
            try:
                if os.path.exists(path):
                    self.sounds[sound_name] = pygame.mixer.Sound(path)
                    print(f"Successfully loaded {sound_name} sound from: {path}")
                    return True
            except Exception as e:
                print(f"Failed to load {sound_name} sound from {path}: {e}")
        
        print(f"Could not find any {sound_name} sound files")
        return False
    
    def play_music(self, music_name):
        """Play background music"""
        music_path = resource_path(os.path.join('assets', 'sounds', f'{music_name}.mp3'))
        
        # Check if music file exists
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0 if self.muted else self.music_volume)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            except Exception as e:
                print(f"Error playing music: {e}")
        else:
            # Create placeholder music using pygame's built-in synth
            self.create_placeholder_music()
    
    def create_placeholder_music(self):
        """Create a simple placeholder music using pygame's synth"""
        try:
            # This is a simple placeholder that creates a basic synth sound
            # In a real game, you'd use actual music files
            pygame.mixer.music.load(self.generate_placeholder_music())
            pygame.mixer.music.set_volume(0 if self.muted else self.music_volume * 0.5)
            pygame.mixer.music.play(-1)
        except:
            print("Could not create placeholder music.")
    
    def generate_placeholder_music(self):
        """Generate a simple music file using pygame's synth capabilities"""
        # This is a very basic placeholder - in a real game you'd use actual music files
        # This creates a simple sine wave pattern
        try:
            import numpy as np
            from io import BytesIO
            
            sample_rate = 44100
            duration = 5.0  # 5 seconds
            
            # Generate a simple melody
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create a simple melody pattern
            notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # C4 to C5
            melody = np.zeros_like(t)
            
            note_duration = 0.5  # half a second per note
            for i, note in enumerate(notes):
                start = int(i * note_duration * sample_rate)
                end = int((i + 1) * note_duration * sample_rate)
                if end > len(t):
                    break
                melody[start:end] = np.sin(2 * np.pi * note * t[start:end])
            
            # Convert to 16-bit PCM
            melody = (melody * 32767).astype(np.int16)
            
            # Save to a BytesIO object
            buffer = BytesIO()
            import wave
            with wave.open(buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(melody.tobytes())
            
            buffer.seek(0)
            return buffer
        except ImportError:
            # If numpy is not available, create a simple beep sound
            print("NumPy not available, creating simple beep sound")
            from array import array
            from math import sin, pi
            
            sample_rate = 44100
            duration = 1.0  # 1 second
            volume = 0.5
            
            # Generate a simple sine wave
            n_samples = int(sample_rate * duration)
            sound_buffer = array("h", [0] * n_samples)
            
            for i in range(n_samples):
                sample = int(volume * 32767.0 * sin(2 * pi * 440 * i / sample_rate))
                sound_buffer[i] = sample
            
            # Save to a BytesIO object
            from io import BytesIO
            buffer = BytesIO()
            import wave
            with wave.open(buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(sound_buffer.tobytes())
            
            buffer.seek(0)
            return buffer
    
    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            print(f"Playing sound: {sound_name}")
            self.sounds[sound_name].play()
    
    def toggle_mute(self):
        """Toggle mute/unmute for background music only"""
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0 if self.muted else self.music_volume)
        print("Music muted" if self.muted else "Music unmuted")
    
    def get_music_status(self):
        """Get a string representing the current music status"""
        return "MUTED" if self.muted else "ON"
