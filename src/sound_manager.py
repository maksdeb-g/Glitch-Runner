import pygame
import os

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Set volume levels
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        
        # Dictionary to store sound effects
        self.sounds = {}
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all game sounds"""
        sound_path = os.path.join('assets', 'sounds')
        
        # Check if sound files exist and load them
        try:
            # Sound effects
            if os.path.exists(os.path.join(sound_path, 'jump.wav')):
                self.sounds['jump'] = pygame.mixer.Sound(os.path.join(sound_path, 'jump.wav'))
            
            if os.path.exists(os.path.join(sound_path, 'jump-audio.mp3')):
                self.sounds['jump'] = pygame.mixer.Sound(os.path.join(sound_path, 'jump-audio.mp3'))
            
            if os.path.exists(os.path.join(sound_path, 'land.wav')):
                self.sounds['land'] = pygame.mixer.Sound(os.path.join(sound_path, 'land.wav'))
            
            if os.path.exists(os.path.join(sound_path, 'glitch.wav')):
                self.sounds['glitch'] = pygame.mixer.Sound(os.path.join(sound_path, 'glitch.wav'))
            
            if os.path.exists(os.path.join(sound_path, 'level_complete.wav')):
                self.sounds['level_complete'] = pygame.mixer.Sound(os.path.join(sound_path, 'level_complete.wav'))
            
            # Game over sound (single death)
            if os.path.exists(os.path.join(sound_path, 'pixel-explosion-319166.mp3')):
                self.sounds['game_over'] = pygame.mixer.Sound(os.path.join(sound_path, 'pixel-explosion-319166.mp3'))
            elif os.path.exists(os.path.join(sound_path, 'game-over.mp3')):
                self.sounds['game_over'] = pygame.mixer.Sound(os.path.join(sound_path, 'game-over.mp3'))
            
            # Final death sound (when out of lives)
            if os.path.exists(os.path.join(sound_path, 'pixel-death-66829.mp3')):
                self.sounds['final_death'] = pygame.mixer.Sound(os.path.join(sound_path, 'pixel-death-66829.mp3'))
            
            # Game completion sound
            if os.path.exists(os.path.join(sound_path, 'goodresult-82807.mp3')):
                self.sounds['game_completed'] = pygame.mixer.Sound(os.path.join(sound_path, 'goodresult-82807.mp3'))
            
            # Set volumes for all sounds
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
                
        except Exception as e:
            print(f"Error loading sounds: {e}")
            print("Continuing without sound effects.")
    
    def play_music(self, music_name):
        """Play background music"""
        music_path = os.path.join('assets', 'sounds', f'{music_name}.mp3')
        
        # Check if music file exists
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
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
            pygame.mixer.music.set_volume(self.music_volume * 0.5)  # Lower volume for generated music
            pygame.mixer.music.play(-1)
        except:
            print("Could not create placeholder music.")
    
    def generate_placeholder_music(self):
        """Generate a simple music file using pygame's synth capabilities"""
        # This is a very basic placeholder - in a real game you'd use actual music files
        # This creates a simple sine wave pattern
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
    
    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
