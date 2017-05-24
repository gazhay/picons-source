#!/bin/bash

noclear=0
boxname="root@vuuno.lan"
noprompt=0
usersyncinstead=0
moreicons=""

while test $# -gt 0; do
  case "$1" in
      -h|--help)
              echo "IPTV Hacky script for Picons"
              echo " "
              echo "iptv.sh [options]"
              echo " "
              echo "options:"
              echo "--no-clear    Doesn't wipe out target box first"
              echo "-y            Doesn't ask for confirmation first"
              echo "--boxname=    Uses specified box as target"
              echo "--rsync-logos Requires rsync on box"
              echo "--more-icons  Upload additional icons from dir"
              exit 0
              ;;
      --no-clear) export noclear=1
          ;;
      -y|--noprompt) export noprompt=1
          ;;
      --boxname*)
          export boxname=`echo $1 | sed -e 's/^[^=]*=//g'`
          shift
          ;;
      --more-icons*)
          export moreicons=`echo $1 | sed -e 's/^[^=]*=//g'`
          shift
          ;;
      --rsync-logos)
          export usersyncinstead=1
          ;;
      --*) echo "bad option $1"
          ;;
      *) break
          ;;
    esac
    shift
done

scriptheader="#!/bin/bash

# Close STDOUT file descriptor
exec 1<&-
# Close STDERR FD
exec 2<&-

# Open STDOUT as file for read and write.
exec 1<>iptvbox.log

# Redirect STDERR to STDOUT
exec 2>&1

"

echo "[TARGET BOX] $boxname"
if [[ $noprompt -lt 1 ]];then
  read -p "Are you sure? " -n 1 -r
  echo    # (optional) move to a new line
fi
if [[ $REPLY =~ ^[Nn]$ ]];then
  echo "Stopped"
  exit 0;
else
  rm -r build-input/enigma2
  echo "[FETCHING bouquets]"
  scp -r root@vuuno.lan:/etc/enigma2 build-input/
  echo "[CLEARING local picons]"
  rm newpicon/*
  echo "" > iptv.log
  echo "$scriptheader" > runonbox.sh
  for file in build-input/enigma2/*userbouquet*tv*; do
    bouquet=$(basename $file)
    echo "Bouquet : $bouquet"
    echo "echo '$bouquet'" >> runonbox.sh
    echo "echo '--------------------------------------------$bouquet'" >> iptv.log
    ./iptv.py $file
  done
  ./iptv-syn.py

  echo "[SUMMARY] --------------------"
  echo -e $(grep FOUND iptv.log | wc -l)
  echo " found icons"
  echo -e $(grep MISSING iptv.log | wc -l)
  echo " missing icons"
  echo "------------------------------"
  if [[ $noclear -lt 1 ]]; then
    echo "[CLEARING Box $boxname]"
    ssh $boxname "rm /media/usb/picon/*" > /dev/null 2>&1
  fi
  echo "[ICON UPLOAD]"
  if [[ $moreicons -eq "" ]];then
    if [[ $usersyncinstead -gt 0 ]];then
      echo "[--rsync newpicons]"
      rsync -avh --ignore-existing newpicon/* $boxname:/media/usb/picon/
    else
      echo "[--scp newpicons]"
      scp newpicon/* $boxname:/media/usb/picon
    fi
  else
    pushd $moreicons
    if [[ $usersyncinstead -gt 0 ]];then
      echo "[--rsync $moreicons]"
      rsync -avh --ignore-existing * $boxname:/media/usb/picon/logos/
    else
      echo "[--scp $moreicons]"
      scp * $boxname:/media/usb/picons/logos/
    fi
    popd
  fi
  echo "[SCRIPT UPLOAD]"
  scp runonbox.sh $boxname:/media/usb/picon
  # scp newpicon/* $boxname:/media/usb/picon
  echo "[SCRIPT EXECUTE]"
  ssh $boxname "chmod +x /media/usb/picon/runonbox.sh && cd /media/usb/picon && ./runonbox.sh"
  echo "[MOVE OTHERS]"
  ssh $boxname "cd /media/usb/picon && mv -n logos/* ."
  echo "[RETRIEVE LOG]"
  scp $boxname:/media/usb/picon/iptvbox.log .
  echo "[DONE.]"
fi
