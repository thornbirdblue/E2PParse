#!/usr/bin/env python

##########################################################################
#	CopyRight	(C)	THORNBIRD,2030	All Rights Reserved!
#
#	Module:		Scan Excel File
#
#	File:		e2pparse.py
#
#	Author:		thornbird
#
#	Date:		2022-04-12
#
#	E-mail:		wwwthornbird@163.com
#
###########################################################################

###########################################################################
#
#	History:
#	Name		Data		Ver		Act
#--------------------------------------------------------------------------
#	thornbird	2022-04-12	v1.0		create
#
###########################################################################

import sys,os,re,string,time,datetime
import pandas as pd

SW_VERSION='0.1'

ConfigFile=[]

DefaultScanFileType=('.xlsx','.csv')

ScanPath=''

# log var
debugLog = 0
debugLogLevel=(0,1,2,3)	# 0:no log; 1:op logic; 2:op; 3:verbose

class FileScan:
        Tags = 'FileScan'
        __dirname=''
        __filename=''
        __fd=''

        __fileLines=0

        __timeFormat=r'\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'        

        __beginTime=''
        __endTime=''

        __KeyWordsNum=0
        __KeyWords=[]

        def __init__(self,dirname,filename,fd):
            self.__dirname=dirname
            self.__filename=filename
            self.__fd=fd
            self.__fileLines=0
            
            self.__KeyWordsNum=0
            self.__KeyWords=[]

        def __get_key (self,dict, value):
            return [k for k, v in dict.items() if v == value]

        def __CheckKeyWords(self,line,KeyWords):
            if debugLog >= debugLogLevel[-1]:
                print('CheckKeyWords: '+line,KeyWords)

            for i in range(0,len(KeyWords)):
                
                m = re.search(KeyWords[i],line)
                if m:
                    self.__KeyWordsNum += 1
                    self.__KeyWords.append(line)
                    
                    if debugLog >= debugLogLevel[2]:
                        print('(WARN) Find KeyWord: '+line)

        def Check(self,Flows):
            if debugLog >= debugLogLevel[-1]:
                print('CheckLogs: ',self.__filename)
                        

        def __SaveFile(self,filename,datas):
            if len(datas):
                try:
                    fd = open(os.path.join(self.__dirname,filename),'wt')
                
                    for i in range(0,len(datas)):
                        fd.write(datas[i])
                except IOError:
                    print( "Error: Can't open or write!!!")
                else:
                    fd.close()
                    print( 'Save file: '+self.__dirname+'\\'+filename)
            else:
                if debugLog >= debugLogLevel[2]:
                    print( '(WARN) Save File len is 0!')

        def SaveToFile(self,fd):
            if debugLog >= debugLogLevel[-1]:
                print( 'SaveToFile:')

            if self.__logLines:
                fd.write(self.__dirname+'\n')
                fd.write(self.__filename+': '+str(self.__logLines)+'\n')

                fd.write('BeginTime: '+self.__beginTime+'\n')
                fd.write('EndTime  : '+self.__endTime+'\n')

                fd.write('4.KeyWordsNum  : '+str(self.__KeyWordsNum)+'\n')
                fd.write('\n')

                self.__SaveFile(self.Tags+'_KeyWords_'+self.__filename,self.__KeyWords)
                self.__SaveFile(self.Tags+'_CamFlows_'+self.__filename,self.__CameraFlows)

        def Dump(self):
            if debugLog >= debugLogLevel[-1]:
                print( 'Dump:')

            if self.__logLines:
                print( self.__filename+': '+str(self.__logLines))

                print( 'BeginTime: '+self.__beginTime)
                print( 'EndTime  : '+self.__endTime+'\n')

                print( '4.KeyWordsNum  : '+str(self.__KeyWordsNum))

        def getFileName(self):
            return os.path.join(self.__dirname,self.__filename)

        def getLogLines(self):
            return self.__logLines

#Global Data
class ScanFileType:
        global DefaultScanFileType

        __Scans={}
        __ScanFiles=DefaultScanFileType

        def SetScanTags(self,Class,ScanTags):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Set ScanDirs : ',ScanTags)
            self.__Scans[Class]=ScanTags

        def SetScanFiles(self,ScanFiles):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Set ScanFiles : ',ScanFiles)
            self.__ScanFiles=ScanFiles
        
        def GetScanFiles(self):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Get ScanFiles')
            return self.__ScanFiles

        def GetScans(self):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Get KeyWords ')
            return self.__Scans

        def Dump(self):
            print( 'Scans: ',self.__Scans)

#global var
ScanFiles = ScanFileType()
Datas=[]

def FileCheck(dirname,filename,fd):
    if debugLog >= debugLogLevel[-1]:
        print( 'Scan Log:  '+filename)

    fScan = FileScan(dirname,filename,fd)
    print(fd)
    #fScan.Check(ScanFiles.GetTags())

    #Datas.append(fScan)

def ScanFile(dirname,file):
    if debugLog >= debugLogLevel[-1]:
        print( 'Scan File:\n '+dirname+file)

    if debugLog >= debugLogLevel[2]:
        print( "(INFO) Match File Type: ",ScanFiles.GetScanFiles())
    
    Types = ScanFiles.GetScanFiles()

    #for file in files:

    for i in range(0,len(Types)):
        if debugLog >= debugLogLevel[-1]:
            print( "File Match Format: "+Types[i])
      
          
        fileType = re.compile(Types[i])

        if debugLog >= debugLogLevel[-1]:
            print( file)
		
        m = re.search(fileType,file)
        if m:
            path,name = os.path.split(dirname)

            if debugLog >= debugLogLevel[-1]:
                print( 'Find Dir: '+dirname)
		
            if debugLog >= debugLogLevel[1]:
                print( 'Find Match File: '+file)

            try:
                #fd = open(os.path.join(dirname,file),'rb')
			
                if debugLog >= debugLogLevel[-1]:
                       print( 'INFO: open file :'+os.path.join(dirname,file))

                fd = pd.read_exce(os.path.join(dirname,file),'rb')
                FileCheck(dirname,file,fd)

                #fd.close()

            except IOError:
                print( "open file ERROR: Can't open"+os.path.join(dirname,file))

def SaveData(filename,datas):
    if debugLog >= debugLogLevel[-1]:
        print( 'SaveData Begin: ',filename)

    try:
        fo = open(filename,"wt")

        fo.write('Scan Total Files: '+str(len(datas))+'\n')
        
        fo.write('Files:\n')
        for i in range(0,len(datas)):
            fo.write(datas[i].getFileName()+'\n')
        fo.write('\n\n')

        for i in range(0,len(datas)):
            datas[i].SaveToFile(fo)

    except IOError:
        print( "Error: Can't open or write!!!")
    else:
        fo.close()

        print( '\nSaveFile: ',filename)

def ScanDir(Dir):
    CamDirs=[]
    print( 'Scan DIR: '+Dir+'\n')

    #os.path.walk(Dir,ScanFile,())
    #print(os.listdir(Dir))
    with os.scandir(Dir) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                ScanFile(Dir,entry.name)


def ParseArgv():
	if len(sys.argv) > appParaNum+1:
		HelpInfo()
		sys.exit()
	else:
		for i in range(1,len(sys.argv)):
			if sys.argv[i] == '-h':
				Usage()
				sys.exit()
			elif sys.argv[i] == '-d':
				if sys.argv[i+1]:
					debug = int(sys.argv[i+1])
					if type(debug) == int:
						global debugLog
						debugLog = debug						
						print( 'Log level is: '+str(debugLog))
					else:
						print( 'cmd para ERROR: '+sys.argv[i+1]+' is not int num!!!')
				else:
					CameraOpenKPIHelp()
					sys.exit()
			elif sys.argv[i] == '-o':
				if sys.argv[i+1]:
					global fileName
					fileName = sys.argv[i+1]
					print( 'OutFileName is '+fileName)
				else:
					Usage()
					sys.exit()
			elif sys.argv[i] == '-p':
				if sys.argv[i+1]:
					global ScanPath
					ScanPath = sys.argv[i+1]
					print( 'Scan dir path is '+ScanPath)
				else:
					Usage()
					sys.exit()
			elif sys.argv[i] == '-c':
				if sys.argv[i+1]:
					global ConfigFile
					ConfigFile = sys.argv[i+1]
					print( 'ConfigFile is '+ConfigFile)
				else:
					Usage()
					sys.exit()


def Usage():
	print( 'Command Format :')
	print( '		CameraLogScan [-d 1/2/3] [-o outputfile] [-p path]  [-c configfile] [-z(unzip zip files)]| [-h]')

appParaNum = 6

if __name__ == '__main__':
        print( 'Version: '+SW_VERSION)

        ParseArgv()

        if not ScanPath.strip():
                spath = os.getcwd()
        else:
                spath = ScanPath

        ScanDir(spath)
