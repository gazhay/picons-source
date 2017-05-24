#!/usr/bin/python -u

from __future__ import print_function

runonbox = open("runonbox.sh",'a')
debuglog = open("iptv.log","a")

forcehdtoo = True

synonyms={
    "bbcone":[ "bbconescot", "bbconelon", "bbconeci", "bbconeemid", "bbconeeaste", "bbconeeastw", "bbconenwest", "bbconeneandc", "bbconeni", "bbconeoxford", "bbconeseast", "bbconesouth", "bbconeswest", "bbconewmid", "bbconewales", "bbconewest", "bbconeyorks", "bbconeykandli", "bbconehd", "bbconescothd", "bbconewalhd", "bbconenihd" ],
    "bbctwo":[ "bbctwoeng", "bbctwoni", "bbctwoscot", "bbctwowales" ],
    "stvhd" :[ "stvtwo", "stv2" ],
    "itv2"  :[ "itv2plus1", "itvtwoplusone" ],
    "itv3"  :[ "itv3plus1", "itvthreeplusone" ],
    "itvbe" :[ "itvbeplus1", "itvbeplusone" ],
    "channel4" :[ "channel4plus1", "channelfourplusone" ],
    "e4"    :[ "e4plus1", "efourplusone" ],
    "more4" :[ "more4plus1", "morefourplusone" ],
    "channel5":["channel5plus1", "channelfiveplusone"],
    "5usa"  :["5usaplus1"],
    "5star" :["5starplus1"],
    "sky1"  :["skyone"],
    "sky2"  :["skytwo"]
}

print("Adding synonyms", file=debuglog)
print("echo 'Adding synonyms'", file=runonbox)
for syn in synonyms:
    # add hd variant of original
    if forcehdtoo:
        print("ln -s "+syn+".png "+syn+"hd.png", file=runonbox)
    for thissyn in synonyms[syn]:
        # add variants
        print("ln -s "+syn+".png "+thissyn+".png", file=runonbox)
        if forcehdtoo:
            # hd varaints
            print("ln -s "+syn+".png "+thissyn+"hd.png", file=runonbox)
