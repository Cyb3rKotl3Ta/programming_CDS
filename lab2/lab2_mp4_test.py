import cv2
import pyaudio
import wave
from pydub import AudioSegment

# Video parameters
width, height = 640, 480
frame_rate = 30
video_filename = 'output_video.mp4'  # Changed file extension to MP4

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
audio_filename = "output_audio.mp3"  # Changed file extension to MP3

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize video writer for MP4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change the codec to mp4v for MP4
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

# Convert audio frames to MP3 and save to file
audio_data = b''.join(frames)
audio_segment = AudioSegment(
    audio_data, 
    frame_rate=RATE, 
    sample_width=audio.get_sample_size(FORMAT), 
    channels=CHANNELS
)
audio_segment.export(audio_filename, format="mp3")

print('Video saved as', video_filename)
print('Audio saved as', audio_filename)
