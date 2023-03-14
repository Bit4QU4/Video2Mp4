#Code designed to iterate through a directory and convert video files to .mp4 format
#import libaries
import os
import subprocess
import sys
import zipfile
import ctypes
import filetype
import logging
from tqdm import tqdm

global directory 
directory = input("Directory to Convert: ")
logging.basicConfig(format='%(asctime)s %(message)s', level = logging.DEBUG, filename="OutLog - " + directory)

class VidConvert:
    def ffmpeg_convert(video_input,video_output):
        #try to start ffmpeg exe from comandline
        try:
            command = ['ffmpeg','-i', video_input, video_output, '-hide_banner', '-n' , '-preset', 'slow']
            subprocess.call(command, shell=True)
        #if the process errors out then print
        except:
            print("ffmpeg failure, double check install")
            logging.CRITICAL("ffmpeg is unavailable! Double check install")

    def directory_iteration(directory):
        #set working directory
        os.chdir(directory)
        #set base count
        count = 0
        #shows the user that something is happening
        print("Files Converted: " + str(count))
        #iterate through files in directory specified
        for filename in tqdm(os.listdir(directory)):
            if os.path.isdir(filename):
                logging.DEBUG("directory found, skipping")
            #if statements to catch files that are already mp4
            elif os.path.splitext(filename)[1] == '.mp4':
                logging.INFO(filename + " Already in mp4 format")
            elif 'Convert_' in os.path.splitext(filename)[0]:
                logging.INFO("Folder Already Contains an Output Zip, operation done?")
                sys.exit()
            elif filetype.guess(filename) == None:
                logging.WARNING("Unable to parse filetype" + filename)
            elif "video" in filetype.guess(filename).mime:
                 input = str(os.path.abspath(directory)) + '\\' + str(os.path.basename(filename))
                 output = str(os.path.abspath(directory)) + '\\' + str(os.path.splitext(filename)[0]) + '_converted.mp4'
                 #calls the converting function
                 VidConvert.ffmpeg_convert(input,output)
                 #sends converted files to a centeral zip file
                 VidConvert.ZipUp(str(os.path.splitext(filename)[0]) + '_converted.mp4',directory)
                 #updates the count set earlier, keep track of how many files have been Converted
                 count = count + 1
                 #logs some output
                 logging.DEBUG("File Selected-" + input)
                 logging.DEBUG("Current Count of File-" + str(count))
                 logging.DEBUG("File Finished Converting")
            else:
                print('File not video/unrecognizable')
                logging.INFO("File not video -- skipping: "+ filename)
        #makes a message box to inform user that task has been completed
        ctypes.windll.user32.MessageBoxW(0, "Done, Files Converted: " + str(count), "Conversion Complete", 0x40 | 0x0)
    #Cleans up left over files after they are coppied to the zipfile
    def cleanup(directory):
        for filename in os.listdir(directory):
            if '_converted' in os.path.splitext(filename)[0]:
                os.remove(filename)
            elif 'OutLog - ' in os.path.splitext(filename)[0]:
                os.remove(filename)
            else:
                print("File Untouched :" + filename)
    #Zips whatever is given as input and appends to 'Convert_of_' file
    def ZipUp(input,directory):
        zip = zipfile.ZipFile('Convert_of_'+ str(os.path.basename(directory)) +'.zip','a')
        zip.write(input)
        zip.close()
#main loop
def main(directory):
    VidConvert.directory_iteration(directory)
    VidConvert.ZipUp("log_" +str(os.path.basename(directory))+ ".txt",directory)
    VidConvert.cleanup(directory)
if __name__ == '__main__':
    main(directory)
