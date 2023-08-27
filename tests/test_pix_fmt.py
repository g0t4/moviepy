# -*- coding: utf-8 -*-
"""Video file clip tests meant to be run with pytest."""
import os
import sys

import pytest

from moviepy.utils import close_all_clips
from moviepy.video.compositing.CompositeVideoClip import clips_array
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ColorClip

from .test_helper import TMP_DIR
from .test_ffprobe import ffprobe_stream


def test_read_pix_fmt_defaults_to_rgb24():
    clip = VideoFileClip('media/big_buck_bunny_432_433.webm')
    assert clip.reader.pix_fmt == 'rgb24'
    assert clip.reader.depth == 3

    # check frame size
    frame0 = clip.get_frame(0)
    assert frame0.shape == (720, 1280, 3)

    close_all_clips(locals())


def test_read_pix_fmt_yuv444p():
    clip = VideoFileClip('media/big_buck_bunny_432_433.webm', pix_fmt='yuv444p')
    assert clip.reader.pix_fmt == 'yuv444p'
    assert clip.reader.depth == 3

    # check frame size
    frame0 = clip.get_frame(0)
    assert frame0.shape == (720, 1280, 3)
    # ffmpeg -pix_fmts  # list supported formats w/ # components (ie 3 for yuv444p and rgb24), BPP (per pixel) and BIT_DEPTH (bpc - per component)

    # todo convert to rgb24 and compare?
    close_all_clips(locals())


def test_write_pix_fmt_rgb24_to_yuv420p():
    clip = VideoFileClip('media/big_buck_bunny_432_433.webm')
    assert clip.reader.pix_fmt == 'rgb24'

    tmp_video_output = os.path.join(TMP_DIR, "test.mp4")
    clip.write_videofile(tmp_video_output, codec='libx264', output_pix_fmt='yuv420p')

    entries = ffprobe_stream(tmp_video_output)
    assert entries['pix_fmt'] == 'yuv420p'


# TODO yuv422p (depth is 2) and yuv420p (depth is 1.5), requires further testing (esp around reading frames)

if __name__ == '__main__':
    pytest.main()
