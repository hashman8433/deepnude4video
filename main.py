import sys
import cv2
import os
sys.path.append(os.path.join(os.path.dirname(__file__), './lib'))
from run import process
import ffmpeg
import numpy as np

def deep_nude_process(dress):
	h = dress.shape[0]
	w = dress.shape[1]
	dress = cv2.resize(dress, (512,512), interpolation=cv2.INTER_CUBIC)
	watermark = process(dress)
	watermark = cv2.resize(watermark, (w,h), interpolation=cv2.INTER_CUBIC)
	return watermark

def process_video(input_path, output_path):
	# https://github.com/kkroening/ffmpeg-python/tree/master/examples
	probe = ffmpeg.probe(input_path)
	video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
	width = int(video_stream['width'])
	height = int(video_stream['height'])

	process1 = (
		ffmpeg
		.input(input_path)
		.output('pipe:', format='rawvideo', pix_fmt='rgb24')
		.run_async(pipe_stdout=True)
	)

	process2 = (
		ffmpeg
		.input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
		.output(output_path, pix_fmt='yuv420p')
		.overwrite_output()
		.run_async(pipe_stdin=True)
	)

	while True:
		in_bytes = process1.stdout.read(width * height * 3)
		if not in_bytes:
			break
		in_frame = (
			np
			.frombuffer(in_bytes, np.uint8)
			.reshape([height, width, 3])
		)

		out_frame = deep_nude_process(in_frame)

		process2.stdin.write(
			out_frame
			.astype(np.uint8)
			.tobytes()
		)

	process2.stdin.close()
	process1.wait()
	process2.wait()

if __name__ == '__main__':
	in_path, out_path = sys.argv[1:3]
	print("Input video:", in_path)
	print("Output video:", out_path)
	process_video(in_path, out_path)
