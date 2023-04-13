from vidstream import CameraClient
from vidstream import VideoClient
from vidstream import ScreenShareClient

# Choose One

client3 = ScreenShareClient('127.0.0.1', 9999,1920,1080)


client3.start_stream()