#!/bin/bash

itrSeq=$1
workingDir=$2

muscle -clw -quiet -in $workingDir/$itrSeq -out $workingDir/align_$itrSeq.fasta &>/dev/null
