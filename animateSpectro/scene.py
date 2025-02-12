#!/usr/bin/env python3
import argparse
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import AudioFileClip, VideoClip

def make_frame_factory(image, start, end, audio_duration, line_height, line_thickness):
    width, height = image.size
    def make_frame(t):
        # Compute normalized time (clamped by audio_duration)
        fraction = t / audio_duration if audio_duration > 0 else 0
        # Interpolate position between start and end
        x_norm = (1 - fraction) * start[0] + fraction * end[0]
        y_norm = (1 - fraction) * start[1] + fraction * end[1]
        # Convert normalized coordinates to pixel coordinates.
        pixel_x = int(x_norm * (width - 1))
        pixel_y = (height - 1) - int(y_norm * (height - 1))
        # Create an RGBA copy of the image and an overlay for the vertical line.
        frame_img = image.copy().convert("RGBA")
        overlay = Image.new("RGBA", frame_img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        # Determine rectangle coordinates for the vertical line.
        left = pixel_x - line_thickness // 2
        right = pixel_x + line_thickness // 2
        top = pixel_y - line_height // 2
        bottom = pixel_y + line_height // 2
        # Draw a semi-transparent red rectangle (faint vertical line).
        draw.rectangle((left, top, right, bottom), fill=(0, 0, 0, 128))
        # Composite the overlay on the background.
        new_frame = Image.alpha_composite(frame_img, overlay)
        return np.array(new_frame.convert("RGB"))
    return make_frame

def main():
    parser = argparse.ArgumentParser(
        description="Create a video with a moving faint red vertical line over a static PNG background with synced audio."
    )
    parser.add_argument("audio_file", help="Path to the audio file")
    parser.add_argument("png_file", help="Path to the PNG file")
    parser.add_argument("--start", nargs=2, type=float, required=True,
                        metavar=("START_X", "START_Y"),
                        help="Normalized start position (0-1 for both x and y)")
    parser.add_argument("--end", nargs=2, type=float, required=True,
                        metavar=("END_X", "END_Y"),
                        help="Normalized end position (0-1 for both x and y)")
    parser.add_argument("--frames", type=int, required=True,
                        help="Total number of frames to generate (used to set fps)")
    parser.add_argument("--output", default="output.mp4",
                        help="Output video filename (default: output.mp4)")
    parser.add_argument("--line_height", type=int, default=20,
                        help="Height of the vertical line in pixels (default: 20)")
    parser.add_argument("--line_thickness", type=int, default=3,
                        help="Thickness of the vertical line in pixels (default: 3)")
    args = parser.parse_args()
    
    # Load the background image and audio clip.
    image = Image.open(args.png_file).convert("RGB")
    audio_clip = AudioFileClip(args.audio_file)
    audio_duration = audio_clip.duration

    # Calculate fps such that total frames roughly equals args.frames.
    fps = args.frames / audio_duration if audio_duration > 0 else 1

    # Create the frame generation function.
    make_frame = make_frame_factory(image, args.start, args.end, audio_duration,
                                    args.line_height, args.line_thickness)
    
    # Create a video clip that computes frames on the fly.
    video_clip = VideoClip(make_frame, duration=audio_duration)
    video_clip = video_clip.set_audio(audio_clip)
    
    # Write the output video file.
    video_clip.write_videofile(args.output, codec="libx264", audio_codec="aac", fps=fps)

if __name__ == "__main__":
    main()



## python3 scene.py audio.wav spectrogram.png --start 0.067 0.47 --end 0.842 0.47 --frames 44 --output my_video.mp4 --line_height 300 --line_thickness 1
