#!/bin/bash

cd $1
paste score_itr1.tmp score_itr2.tmp | awk 'NR==1{print "Score_ITRs_vs_consensus"} NR>1 { print ($1+$2)/2}' > score_itrs.tmp
