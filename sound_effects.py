#!/usr/bin/env python3
"""
Computer Sound Effects Generator
Creates authentic retro computer sounds using waveform synthesis
"""

import math
import wave
import struct
import io

class SoundEffects:
    """Generate retro computer sound effects"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
    def generate_tone(self, frequency, duration, volume=0.3):
        """Generate a pure tone"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            sample = volume * math.sin(2 * math.pi * frequency * t)
            samples.append(sample)
        
        return samples
    
    def generate_beep(self, frequency=800, duration=0.1, volume=0.3):
        """Generate a simple beep sound"""
        return self.generate_tone(frequency, duration, volume)
    
    def generate_click(self, duration=0.02, volume=0.5):
        """Generate a click sound (like relay or switch)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            # Sharp attack, quick decay
            envelope = math.exp(-10 * i / num_samples)
            noise = (hash(i) % 1000 - 500) / 500.0  # Pseudo-random noise
            sample = volume * noise * envelope
            samples.append(sample)
        
        return samples
    
    def generate_pong_sound(self, duration=0.05, volume=0.4):
        """Generate classic pong/printer sound"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        # Start high, drop quickly (like mechanical impact)
        for i in range(num_samples):
            t = i / self.sample_rate
            # Frequency sweep from 1200Hz to 200Hz
            freq = 1200 - (1000 * i / num_samples)
            envelope = math.exp(-8 * i / num_samples)
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
        
        return samples
    
    def generate_printer_sound(self, duration=0.08, volume=0.3):
        """Generate dot matrix printer sound"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Multiple frequencies for mechanical sound
            freq1 = 400 + 200 * math.sin(50 * t)
            freq2 = 800 + 100 * math.sin(30 * t)
            envelope = math.exp(-5 * i / num_samples)
            
            sample = volume * envelope * (
                0.5 * math.sin(2 * math.pi * freq1 * t) +
                0.3 * math.sin(2 * math.pi * freq2 * t)
            )
            samples.append(sample)
        
        return samples
    
    def generate_read_sound(self, duration=0.03, volume=0.3):
        """Generate memory read sound (high pitch click)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = 2000 - (1500 * i / num_samples)
            envelope = math.exp(-15 * i / num_samples)
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
        
        return samples
    
    def generate_write_sound(self, duration=0.04, volume=0.3):
        """Generate memory write sound (lower pitch click)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = 800 - (400 * i / num_samples)
            envelope = math.exp(-12 * i / num_samples)
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
        
        return samples
    
    def generate_load_sound(self, duration=0.5, volume=0.25):
        """Generate program loading sound (ascending tones)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Ascending frequency sweep
            freq = 200 + (800 * i / num_samples)
            envelope = 1.0 - (0.5 * i / num_samples)
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
        
        return samples
    
    def generate_run_sound(self, duration=0.3, volume=0.3):
        """Generate program run sound (quick ascending beep)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = 400 + (1200 * i / num_samples)
            envelope = math.exp(-3 * i / num_samples)
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
        
        return samples
    
    def generate_unload_sound(self, duration=0.4, volume=0.25):
        """Generate program unload sound (descending tones)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Descending frequency sweep
            freq = 1000 - (800 * i / num_samples)
            envelope = 1.0 - (0.7 * i / num_samples)
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
        
        return samples
    
    def generate_error_sound(self, duration=0.2, volume=0.4):
        """Generate error sound (harsh buzz)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Low frequency buzz
            freq = 100
            sample = volume * math.sin(2 * math.pi * freq * t)
            # Add harmonics for harshness
            sample += 0.3 * volume * math.sin(2 * math.pi * freq * 3 * t)
            samples.append(sample)
        
        return samples
    
    def generate_halt_sound(self, duration=0.6, volume=0.3):
        """Generate halt sound (descending tone to silence)"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = 600 - (550 * i / num_samples)
            envelope = 1.0 - (i / num_samples)
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
        
        return samples
    
    def samples_to_bytes(self, samples):
        """Convert samples to 16-bit PCM bytes"""
        byte_data = b''
        for sample in samples:
            # Clamp to [-1, 1] and convert to 16-bit integer
            sample = max(-1.0, min(1.0, sample))
            value = int(sample * 32767)
            byte_data += struct.pack('<h', value)
        return byte_data
    
    def save_wav(self, samples, filename):
        """Save samples as WAV file"""
        byte_data = self.samples_to_bytes(samples)
        
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(byte_data)
    
    def get_wav_data(self, samples):
        """Get WAV data as bytes (for in-memory playback)"""
        byte_data = self.samples_to_bytes(samples)
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(byte_data)
        
        wav_buffer.seek(0)
        return wav_buffer.read()


def generate_all_sounds():
    """Generate all sound effects and save as WAV files"""
    sfx = SoundEffects()
    
    sounds = {
        'beep.wav': sfx.generate_beep(),
        'click.wav': sfx.generate_click(),
        'pong.wav': sfx.generate_pong_sound(),
        'printer.wav': sfx.generate_printer_sound(),
        'read.wav': sfx.generate_read_sound(),
        'write.wav': sfx.generate_write_sound(),
        'load.wav': sfx.generate_load_sound(),
        'run.wav': sfx.generate_run_sound(),
        'unload.wav': sfx.generate_unload_sound(),
        'error.wav': sfx.generate_error_sound(),
        'halt.wav': sfx.generate_halt_sound()
    }
    
    print("Generating sound effects...")
    for filename, samples in sounds.items():
        sfx.save_wav(samples, filename)
        print(f"  Created: {filename}")
    
    print("\nAll sound effects generated!")


if __name__ == '__main__':
    generate_all_sounds()
