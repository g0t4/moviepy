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


def test_read_pix_fmt_defaults_to_rgb24():
    clip = VideoFileClip('media/big_buck_bunny_432_433.webm')
    assert clip.reader.pix_fmt == 'rgb24'
    assert clip.reader.depth == 3
    # todo assertion on frame size?
    close_all_clips(locals())


def test_read_pix_fmt_yuv444p():
    clip = VideoFileClip('media/big_buck_bunny_432_433.webm', pix_fmt='yuv444p')
    assert clip.reader.pix_fmt == 'yuv444p'
    assert clip.reader.depth == 3
    # todo assertions on frame size
    # todo convert to rgb24 and compare?
    close_all_clips(locals())


if __name__ == '__main__':
    pytest.main()
