#parse PSM results to get peptide and protein identifications


#this is written in Python 3 

HelpOutput = """
python ParseTimeTrials.py -f /path/to/file

Required Parameters:
-d   <file>  This is a path to the directory that holds all peptide identifications

Example: python .\ParseTimeTrials.py -f TimeTrial.txt
"""


import os
import sys
import getopt
import string
import math
import numpy




class Series:
    #this holds the data for a single method. the time series
    def __init__(self, MethodName):
        self.MethodName = MethodName
        self.AllData = {} #key = bit_length, value = [time1, time2, time3]
        self.AverageTime = {} #key = bit_length, value = average time from the replicate runs
        self.StdevTime = {} #key = bit_length, value = standard deviation of the time from the replicate runs

    def AddTimePoint(self, BitLength, Time):
        if not BitLength in self.AllData.keys():
            self.AllData[BitLength] = []
        self.AllData[BitLength].append(Time)

    def CalcualteAverageStdev(self):
        #by now all the numbers should be in, so we are just getting out averages
        for BitLength in self.AllData.keys():
            TimeArray = self.AllData[BitLength]
            Average = numpy.mean(TimeArray)
            self.AverageTime[BitLength] = Average
            Stdev = numpy.std(TimeArray)
            self.StdevTime[BitLength] = Stdev




class ParserClass:

    def __init__(self):
        "nothing to put in really"
        self.InputPath = "" # holds the console output of the time trial
        self.SignatureBitSizes = [] # simple array for convenience, keys into the Trials.Times dictionary
        self.Methods = ["original popcount", "adjusted popcount", "tanimoto", "cosine", "euclidean"]
        self.SeriesData = {} # key = method, value = series object


    def Main(self):
        #0. 
        #1. get all the series objects created
        for Method in self.Methods:
            self.SeriesData[Method] = Series(Method)
        #organize all the input data
        self.ParseTimeTrialsFile(self.InputPath)
        for Method in self.Methods:
            self.SeriesData[Method].CalcualteAverageStdev()

    def ParseTimeTrialsFile(self, Path):
        #The structure of this file is a bit unique. so here's a multi-line comment below
        """
        Test 1:
        ==================OPENMP====================
        bits: 1000 =================================
        original gcc popcountll 5335.234200 msec,       Sum     1021579025.000000
        adjusted popcountll     6115.239200 msec,       Sum     1021579025.000000
        tanimoto        7269.646600 msec,       Sum     6865657.910338
        cosine  319034.841900 msec,     Sum     -231.155781
        euclidean       122788.387100 msec,     Sum     2514827639.027687
        bits: 4000 =================================
        original gcc popcountll 21169.335700 msec,      Sum     1431394136.000000
        adjusted popcountll     28672.983800 msec,      Sum     1431394136.000000
        tanimoto        30529.395700 msec,      Sum     6867467.207266
        cosine  1223281.841500 msec,    Sum     103.749399
        euclidean       432559.572800 msec,     Sum     5030604106.216221

        """
        Handle = open(Path, 'r')
        print ("I got this path %s"%Path)
        TrialNum = 0 #this should get incremented each time I get a "Test 1" type of line
        BitSizeInt = 0 
        for Line in Handle:
            FirstFourLetters = Line[:4] # crappy parsing, here I come
            if FirstFourLetters == "Test":
                #now setting a new trial. Grep out that number
                TrialNum = Line.strip().split(" ")[1].replace(":", "")#I'm sorry to put so much on a line
            elif FirstFourLetters == "====":
                continue #don't care
            elif FirstFourLetters == "bits":
                BitSize = Line.split(" ")[1]
                BitSizeInt = int(BitSize)
                #put this into the container
                if not BitSizeInt in self.SignatureBitSizes:
                    self.SignatureBitSizes.append(BitSizeInt)
            elif FirstFourLetters == "orig":
                #parse out the time for original gcc popcount
                Time = self.GetTimeOutOfString(Line, "original gcc popcountll")
                #now save to the object
                CurrSeriesObject = self.SeriesData[self.Methods[0]]
                CurrSeriesObject.AddTimePoint(BitSizeInt, Time)
            elif FirstFourLetters == "adju":
                #parse out the time for adjusted popcount
                Time = self.GetTimeOutOfString(Line, "adjusted popcountll")
                #now save to the object
                CurrSeriesObject = self.SeriesData[self.Methods[1]]
                CurrSeriesObject.AddTimePoint(BitSizeInt, Time)
            elif FirstFourLetters == "tani":
                Time = self.GetTimeOutOfString(Line, "tanimoto")
                #now save to the object
                CurrSeriesObject = self.SeriesData[self.Methods[2]]
                CurrSeriesObject.AddTimePoint(BitSizeInt, Time)
            elif FirstFourLetters == "cosi":
                Time = self.GetTimeOutOfString(Line, "cosine")
                #now save to the object
                CurrSeriesObject = self.SeriesData[self.Methods[3]]
                CurrSeriesObject.AddTimePoint(BitSizeInt, Time)
            elif FirstFourLetters == "eucl":
                Time = self.GetTimeOutOfString(Line, "euclidean")
                #now save to the object
                CurrSeriesObject = self.SeriesData[self.Methods[4]]
                CurrSeriesObject.AddTimePoint(BitSizeInt, Time)


    def GetTimeOutOfString(self, Line, KillString):
        #remove the killString and then parse some stuff
        Step1 = Line.replace(KillString, "")
        Step2 = Step1.strip() #to get rid of the excess spaces in the front
        Step3 = Step2.split(" ")[0]
        Step4 = float(Step3)
        Time = Step4/1000 #to scale by milliseconds and get back seconds
        return Time



       
    def AddFiles(self, FilePath):
        #this is called by the iPython Notebook to mimic the ParseCommandLine() function
        #but from the notebook
        self.InputPath = FilePath


    def ParseCommandLine(self, Arguments):
        (Options, Args) = getopt.getopt(Arguments, "f:")
        OptionsSeen = {}
        for (Option, Value) in Options:
            OptionsSeen[Option] = 1
            if Option == "-f":
                self.InputPath = Value
        
if __name__ == "__main__":
    Robot = ParserClass()
    Robot.ParseCommandLine(sys.argv[1:])
    Robot.Main()
