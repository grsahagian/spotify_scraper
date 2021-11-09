from moviepy.editor import *
import glob


files = sorted(glob.glob('spotify_frames/*.png'))
clip = ImageSequenceClip(files, fps = 24)
clip.write_videofile("SPOTIFY-BCR-2021.mp4", fps = 24)