import subprocess


def test_ffprobe_stream():
    out = ffprobe_stream('media/big_buck_bunny_432_433.webm')
    print(out)  # review test console output to see possibilities
    assert out['pix_fmt'] == "yuv420p"
    assert out['width'] == "1280"
    assert out['height'] == "720"
    assert out['r_frame_rate'] == "24/1"


def ffprobe_stream(video_path, stream="v:0") -> dict[str, str]:
    """
      stream
        parse stream entires for this single stream into a dict, defaults to the first video stream
    """

    result = {}
    try:
        cmd = ['ffprobe', '-hide_banner', '-v', 'error', '-select_streams', stream, '-show_entries', "stream", '-of', 'default=noprint_wrappers=1', video_path]

        ffprobe_output = subprocess.check_output(cmd)

        # output looks like (due to noprint_wrappers=1 which drops STREAM wrapper):
        #   width=1280
        #   height=720
        #   pix_fmt=yuv420p
        #   ...

        stream_entries = ffprobe_output.decode('utf-8').strip().splitlines()
        for line in stream_entries:
            key, value = line.split('=')
            result[key] = value
    except subprocess.CalledProcessError:
        result['error'] = f"Error with ffprobe: {cmd}"
    return result