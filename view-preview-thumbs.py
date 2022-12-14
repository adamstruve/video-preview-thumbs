import os, sys, getopt, subprocess, math

def main(argv):
    # Set the default values
    filename = ""
    width = ""
    height = ""
    clip_length = "00:00:02.0"

    # Get the command-line arguments
    opts, args = getopt.getopt(sys.argv[1:], "f:w:h:")

    # Parse the command-line arguments
    for opt, arg in opts:
        if opt == "-f":
            filename = arg
        elif opt == "-w":
            width = int(arg)
        elif opt == "-h":
            height = int(arg)
        
        if (filename == ""):
            print("Please specify a filename.")
            sys.exit(1)

        # Default width and height to 320x240 if not specified
        if (width == ""):
            width = 320
        if (height == ""):
            height = 240

    # Print the values of the filename, width, and height
    generate_preview_clips(filename, width, height, clip_length)

def get_seconds(filename):
    output = subprocess.run(['ffprobe', '-i', filename, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1'],
                            capture_output=True,
                            text=True)
    seconds = math.ceil(float(output.stdout))
    return seconds

def generate_final_preivew():
    print("Generating final preview")
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'list.txt', 'preview.mp4', '-hide_banner', '-y']
    subprocess.run(command)

    # Remove the temporary files
    os.remove("list.txt")
    for i in range(10):
        os.remove(str(i)+".mp4")


def generate_preview_clips(filename, width, height, clip_length):
    # Generate the preview video
    seconds = get_seconds(filename)
    print(f'The duration of the video is {seconds} seconds.')

    # Get the intervals in which to get the preview clips
    interval = math.floor(seconds // 10)
    print(f'Interval: {interval}')
    first = 1

    file = open("list.txt", "a")
    for i in range(10):
        print(first)
        command = [
            "ffmpeg",
            "-ss", str(first),
            "-i", filename,
            "-vf", "scale="+str(width)+":"+str(height)+":force_original_aspect_ratio=increase,crop="+str(width)+":"+str(height)+"",
            "-an",
            "-t", clip_length,
            str(i)+".mp4",
            "-hide_banner",
            "-y"
        ]

        # Run the command
        subprocess.run(command)
        file.write("file '" + str(i) + ".mp4'\n")
        first = first + interval
    file.close()
    generate_final_preivew()

if __name__ == "__main__":
   main(sys.argv[1:])