import os
import pygame
import librosa
import numpy as np

pygame.init()
pygame.mixer.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Beat Spectra")

clock = pygame.time.Clock()

# Load audio file
audio_file_path = os.path.join("src", "sample_100KB.mp3")
y, sr = librosa.load(audio_file_path)

# Pygame mixer setup
pygame.mixer.music.load(audio_file_path)
pygame.mixer.music.play()

# Visual elements
circles = [{'position': (width // 2, height // 2), 'radius': 30, 'color': (255, 255, 255)}]

# Beat detection parameters
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, units='time')

# Loading bar parameters
loading_bar_width = 400
loading_bar_height = 20
loading_bar_position = (width // 2 - loading_bar_width // 2, height - 40)
loading_bar_color = (0, 255, 0)  # Green color for the filled portion
loading_bar_bg_color = (50, 50, 50)  # Dark gray color for the shaded background

running = True
beat_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Simple beat detection using librosa's onset detection function
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    beat_frames = librosa.time_to_frames(beats, sr=sr)
    
    # Change color on every detected beat
    if beat_counter < len(beat_frames) and pygame.mixer.music.get_pos() >= librosa.frames_to_time(beat_frames[beat_counter], sr=sr) * 1000:
        print(f"Beat detected! Total beats: {beat_counter + 1}")
        beat_counter += 1

        for circle in circles:
            # Change color on beat
            circle['color'] = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

    # Draw circles
    for circle in circles:
        pygame.draw.circle(screen, circle['color'], circle['position'], circle['radius'])

    # Draw loading bar background (shaded portion)
    pygame.draw.rect(screen, loading_bar_bg_color, (loading_bar_position[0], loading_bar_position[1], loading_bar_width, loading_bar_height))

    # Draw filled portion of loading bar
    progress = pygame.mixer.music.get_pos() / 1000  # Current position in seconds
    duration = librosa.get_duration(y=y, sr=sr)  # Total duration of the audio clip
    loading_bar_length = int(progress / duration * loading_bar_width)
    pygame.draw.rect(screen, loading_bar_color, (loading_bar_position[0], loading_bar_position[1], loading_bar_length, loading_bar_height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

    # Check if the music has ended
    if not pygame.mixer.music.get_busy():
        running = False

# Stop the music when the program ends
pygame.mixer.music.stop()

# Quit Pygame
pygame.quit()
