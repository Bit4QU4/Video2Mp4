#Code designed to iterate through a directory and convert video files to .mp4 format
#import libaries
import os
import subprocess
import sys
import fnmatch
import zipfile
import shutil
import ctypes
import datetime
import filetype
#Set variables
directory = input("Directory to Convert: ")

#Set main class
class VidConvert:
    def ffmpeg_convert(video_input,video_output):
        #try to start ffmpeg exe from comandline
        try:
            command = ['ffmpeg','-i', video_input, video_output, '-hide_banner', '-n' , '-preset', 'slow']
            subprocess.call(command, shell=True)
        #if the process errors out then print
        except:
            print("ffmpeg failure, double check install")
    #magic happens here
    def directory_iteration(directory):
        #set working directory
        os.chdir(directory)
        #set base count
        count = 0
        print("Files Converted: " + str(count))
        #iterate through files in directory specified
        for filename in os.listdir(directory):
            if os.path.isdir(filename):
                print('dir found, skiping')
            #if statements to catch files that are already mp4
            elif fnmatch.fnmatch(filename, '*_converted.mp4'):
                done = (filename + " Already Done")
                VidConvert.logger(done,directory)
            elif fnmatch.fnmatch(filename, '*.mp4'):
                format = (filename + " Already in mp4 format")
                VidConvert.logger(format,directory)
            elif fnmatch.fnmatch(filename, 'Convert_*'):
                zip_there = ("Folder Already Contains an Output Zip, operation done?")
                VidConvert.logger(zip_there,directory)
                sys.exit()
            elif filetype.guess(filename) == None:
                print('unable to determine if file is video type')
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
                 VidConvert.logger("File Selected-" + input,directory)
                 VidConvert.logger("Current Count of File-" + str(count),directory)
                 VidConvert.logger("File Finished Converting",directory)
            else:
                print('File not video/ unrecognizable')
        #makes a message box to inform user that task has been completed
        ctypes.windll.user32.MessageBoxW(0, "Done, Files Converted: " + str(count), "Conversion Complete", 0x40 | 0x0)
    #Cleans up left over files after they are coppied to the zipfile
    def cleanup(directory):
        for filename in os.listdir(directory):
            if fnmatch.fnmatch(filename, '*_converted.mp4'):
                os.remove(filename)
            elif fnmatch.fnmatch(filename, 'log_*.txt'):
                os.remove(filename)
            else:
                print("File Untouched :" + filename)
    #Zips whatever is given as input and appends to 'Convert_of_' file
    def ZipUp(input,directory):
        zip = zipfile.ZipFile('Convert_of_'+ str(os.path.basename(directory)) +'.zip','a')
        zip.write(input)
        zip.close()
    #Logs input(x) and places it into a log file for later checking
    def logger(x,directory):
        f= open("log_" +str(os.path.basename(directory))+ ".txt","a+")
        #appends current date and time to file input
        f.write(str(datetime.datetime.now())+": " + x)
        #adds new line character for neat-ness
        f.write("\n")
        f.close()
#main loop
def main(directory):
    VidConvert.directory_iteration(directory)
    VidConvert.ZipUp("log_" +str(os.path.basename(directory))+ ".txt",directory)
    VidConvert.cleanup(directory)
if __name__ == '__main__':
    main(directory)
