from moviepy.editor import AudioFileClip
"""
href: https://blog.csdn.net/qq_34769162/article/details/107910036
"""
my_audio_clip = AudioFileClip("../files/bbiamsheep.mp4")
# my_audio_clip.write_audiofile("e:/chrome/my_audio.wav")
my_audio_clip.write_audiofile("../files/bbiamsheep.mp3")
