import subprocess


def test_ffprobe():
    out = ffprobe_video('media/big_buck_bunny_432_433.webm')
    print(out)
    assert out['pix_fmt'] == "yuv420p"
    assert out['width'] == "1280"
    assert out['height'] == "720"
    assert out['r_frame_rate'] == "24/1"


def ffprobe_video(video_path, stream="v:0") -> dict[str, str]:
    result = {}
    try:
        # ** add other entries as needed
        # list possibilities with: ffprobe -hide_banner -show_entries stream media/big_buck_bunny_432_433.webm 
        entries = ['width', 'height', 'r_frame_rate', 'pix_fmt']
        entries_arg = "stream=" + ','.join(entries)

        cmd = ['ffprobe', '-hide_banner', '-v', 'error', '-select_streams', stream, '-show_entries', entries_arg, '-of', 'default=noprint_wrappers=1', video_path]

        ffprobe_output = subprocess.check_output(cmd)

        # output looks like (due to noprint_wrappers=1 which drops STREAM wrapper):
        #   width=1280
        #   height=720
        #   pix_fmt=yuv420p
        #   ...

        output_lines = ffprobe_output.decode('utf-8').strip().splitlines()
        for line in output_lines:
            key, value = line.split('=')
            result[key] = value
    except subprocess.CalledProcessError:
        result['error'] = f"Error with ffprobe: {cmd}"
    return result