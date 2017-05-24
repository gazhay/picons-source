#!/usr/bin/python -u
from __future__ import print_function

import re, sys, os, subprocess

# Regexp to read multiline bouquet and return service/descriptions
regex=re.compile('(#SERVICE\ )(([0-9A-Fa-f]+\:){10})([^\n])*(\n#DESCRIPTION\ )([^\n]*)')

# Logoloc - where to look for logos
# Compile them fisrt with 1&2, then search output
# Or search the svg ones and do a default conversion
#logoloc = "build-source/logos/"
logolocs=[
"build-output/binaries-srp-full/srp-full.880x528-880x528.light.on.transparent_2017-05-23--20-09-17/logos/",
"build-source/logos/"
]

# Read the file
with open(sys.argv[1], 'r') as myfile:
    data=myfile.read()

# IPTV Provider Channel prefixes
prefixes=("UK: ","IRE: ","USA/CA: ");
# Rytec sometimes adds a suffix to the images
iconsuffixes=("","-clivebesle", "-phibruspel","-wispelutri")
# Harcoded swaps
# Mostly plural names, or abbreviations
swapers={
    "mutv"        :"manchesterunitedtv",
    "mutvhd"      :"manchesterunitedtv",
    "lfctv"       :"liverpoolfctv",
    "rtenews"     :"rtenewsnow",
    "eirsports1"  :"eirsport1",
    "eirsports2"  :"eirsport2",
    "btsports1"   :"btsport1",
    "btsports2"   :"btsport2",
    "btsports3"   :"btsport3",
    "btsportsespn":"btsportespn",
    "nbcsnhd"     :"nbcsportsnetwork",
}

services = regex.findall(data)
# Do the basic finding and cleaning according to picon rules
for i,serv in enumerate(services):
    temp=serv[5]
    storeprefix=""
    suffixagain=""
    for pref in prefixes:
        bef=temp
        temp=temp.replace(pref,"")
        if temp!=bef:
            storeprefix=pref
    temp=temp.replace("\r","")
    temp2=temp
    temp2=re.sub(r'\&'         ,'and' , temp2)
    temp2=re.sub(r'\*'         ,'star', temp2)
    temp2=re.sub(r'\+'         ,'plus', temp2)
    temp3=temp2
    temp3=re.sub(r'1'          ,'one'   , temp3)
    temp3=re.sub(r'2'          ,'two'   , temp3)
    temp3=re.sub(r'3'          ,'three' , temp3)
    temp3=re.sub(r'4'          ,'four'  , temp3)
    temp3=re.sub(r'5'          ,'five'  , temp3)
    temp3=re.sub(r'6'          ,'six'   , temp3)
    temp3=re.sub(r'7'          ,'seven' , temp3)
    temp3=re.sub(r'8'          ,'eight' , temp3)
    temp3=re.sub(r'9'          ,'nine'  , temp3)
    temp3=re.sub(r'0'          ,'zero'  , temp3)
    temp2=temp2.lower()
    bef=temp2
    temp2=re.sub(r'\([^)]*\)'  ,'', temp2)
    if bef!=temp2:
        mymatch=re.search(r'\(([^)]*)\)', bef)
        suffixagain=mymatch.group(0)
    temp2=re.sub(r' '          ,'', temp2)
    temp2=re.sub(r'[^a-z0-9]/' ,'', temp2)
    temp3=temp3.lower()
    temp3=re.sub(r'\([^)]*\)'  ,'', temp3)
    temp3=re.sub(r' '          ,'', temp3)
    temp3=re.sub(r'[^a-z0-9]/' ,'', temp3)
    services[i] = (serv[1].replace(":","_"), temp2, temp3,storeprefix,suffixagain)

# print(services)

# How many in this bouquet
totalServices = len(services)

currentservice=0;
print('Service %d/%d' % (currentservice,totalServices), end='\r')

# Open a file to run on the box when picons are copied
runonbox = open("runonbox.sh",'a')
# runonbox = open("link-"+os.path.basename(os.path.normpath(sys.argv[1]))+".sh",'w')
debuglog = open("iptv.log","a")
for servicenow in services:
    currentservice=currentservice+1
    print('Service %d/%d' % (currentservice,totalServices), end='\r')
    service = servicenow[1]
    if service=="": continue
    haveswapped=""
    if service in swapers:
        haveswapped=service
        service = swapers[service]
    ref = servicenow[0][:-1]
    prefixagain = servicenow[3]
    suffixbrackets = servicenow[4]
    found="";
    potentialnames=[];
    for suffix in iconsuffixes:
        potentialnames.append(service+suffix)
        potentialnames.append(servicenow[2]+suffix)
        if service.endswith("1" ): potentialnames.append(service[:-1]+suffix)
        if service.endswith("hd"): potentialnames.append(service[:-2]+suffix)
    for an in potentialnames:
        for logoloc in logolocs:
            # print("Searching "+logoloc)
            if os.path.isfile(logoloc+an+".png"):
                found=an;
                subprocess.call("cp "+logoloc+an+".png ./newpicon/"+an+".png", shell=True)
            if os.path.isfile(logoloc+an+".default.png"):
                found=an;
                subprocess.call("cp "+logoloc+an+".default.png ./newpicon/"+an+".png", shell=True)
            elif os.path.isfile(logoloc+an+".light.png"):
                found=an;
                subprocess.call("cp "+logoloc+an+".light.png ./newpicon/"+an+".png", shell=True)
            elif os.path.isfile(logoloc+an+".default.svg"):
                found=an;
                subprocess.call("rsvg-convert -w 1000 --keep-aspect-ratio --output ./newpicon/"+an+".png "+logoloc+an+".default.svg", shell=True)
                #subprocess.call("inkscape -w 850 --without-gui --export-area-drawing --export-png=./newpicon/"+an+".default.png ./build-source/logos/"+service+".default.svg > /dev/null 2>&1", shell=True)
            elif os.path.isfile(logoloc+an+".light.svg"):
                found=an;
                subprocess.call("rsvg-convert -w 1000 --keep-aspect-ratio --output ./newpicon/"+an+".png "+logoloc+an+".light.svg", shell=True)
                #subprocess.call("inkscape -w 850 --without-gui --export-area-drawing --export-png=./newpicon/"+an+".default.png ./build-source/logos/"+service+".default.svg > /dev/null 2>&1", shell=True)
            if found!="": break
        if found!="": break
    if found!="":
        print("FOUND "+found+" REF "+ref, file=debuglog)
        if ref!="1_0_1_0_0_0_0_0_0_0":
            print("ln -s "+found+".png "+ref+".png", file=runonbox)
        if prefixagain!="" or suffixbrackets!="":
            fname=found.replace("-","")
            if haveswapped!="":
                fname=haveswapped
            myprefix=prefixagain.lower()
            mysuffix=suffixbrackets.lower()
            myprefix=myprefix.replace(":","").replace("/","").replace(" ","")
            mysuffix=mysuffix.replace(":","").replace("/","").replace(" ","").replace("(","").replace(")","")
            print("ln -s "+found+".png "+myprefix+fname+mysuffix+".png", file=runonbox)
            print("  SPECIAL CASE "+myprefix+fname+mysuffix, file=debuglog)
        # if haveswapped!="":
        #     print("ln -s "+found+".png "+haveswapped+".png", file=runonbox)
        #     print("  SWAP CASE "+haveswapped, file=debuglog)
    else:
        print("MISSING "+service, file=debuglog)

print('Service %d/%d' % (currentservice,totalServices), end='\n')
runonbox.close();
debuglog.close();
