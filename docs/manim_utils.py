from manim import *
import requests
from IPython.display import HTML, display, clear_output
import logging
import re
import io

def start():
    logging.basicConfig(level=logging.INFO)
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.INFO)
    logger = logging.getLogger('manim')
    logger.addHandler(ch)
    return log_capture_string, ch, logger

def render_scene_with_quality(scene_class, quality_flag):
    log_capture_string, ch, logger = start()
    config.flush_cache = True
    config.pixel_height, config.pixel_width, config.frame_rate = q_dict[quality_flag]
    scene = scene_class()
    show(quality_flag, scene, log_capture_string)

q_dict = {'-ql': (480, 854, 15), '-qm': (720, 1280, 30), '-qh': (1080, 1920, 60), '-qk': (2160, 3840, 60)}

def show(quality_flag, sc, log_capture_string):
    config.flush_cache = True
    scene = sc
    scene.render()

    log_contents = log_capture_string.getvalue()
    file_path_match = re.search(r"File ready at '(.+?)'", log_contents)

    if file_path_match:
        file_path = file_path_match.group(1)
        print(f"Video saved to {file_path}")

        def upload_file(file_path):
            with open(file_path, 'rb') as f:
                response = requests.post('https://transfer.sh/', files={'file': f})
                if response.status_code == 200:
                    return response.text.strip()
            return None

        video_url = upload_file(file_path)

        clear_output(wait=True)

        if video_url:
            display(HTML(f"""
            <div style="width: 100%;">
              <video width="100%" controls>
                  <source src="{video_url}" type="video/mp4">
                  Your browser does not support the video tag.
              </video>
            </div>
            """))
    else:
        print("Could not find the video file path in Manim's output.")