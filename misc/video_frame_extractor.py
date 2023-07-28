import cv2

def extract_frames(video_path, output_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(f"{output_path}/frame{count}.jpg", image)
        success, image = vidcap.read()
        count += 1

workingdir = "D:\\User Files\\Documents\\University\\Misc\\4th Year Work\\Semester 7\\EE596\\EE506 Miniproject"
inputfile = f"{workingdir}\\Videos\\GI_trimmed.mp4"
outputdir = f"{workingdir}\\Output\\Frames"
# Example usage
extract_frames(inputfile,outputdir)
