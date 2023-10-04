import cv2
import pyaudio
import wave

# Video parameters
width, height = 640, 480
frame_rate = 30
video_filename = 'output_video.avi'

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
audio_filename = "output_audio.wav"

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_filename, fourcc, frame_rate, (width, height))

# Initialize audio recording
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

# Record video and audio
try:
    frames = []
    while True:
        # Capture frame from camera
        ret, frame = cap.read()
        if not ret:
            break

        # Write the frame to the output video
        out.write(frame)

        # Record audio
        audio_frame = stream.read(CHUNK)
        frames.append(audio_frame)

        # Display the frame
        cv2.imshow('Camera', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    stream.stop_stream()
    stream.close()
    audio.terminate()

# Save audio to a file
frames = b''.join(frames)
with wave.open(audio_filename, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(frames)

print('Video saved as', video_filename)
print('Audio saved as', audio_filename)


from moviepy.editor import VideoFileClip, AudioFileClip

# Load the video and audio files
video = VideoFileClip('output_video.avi')  # Replace 'video.mp4' with your video file
audio = AudioFileClip('output_audio.wav')  # Replace 'audio.wav' with your audio file

# Set the audio of the video to the loaded audio file
video = video.set_audio(audio)

# Write the combined video with audio to a file
video.write_videofile('combined_video.mp4', codec='libx264')

# Close the video and audio clips
video.close()
audio.close()