#!/bin/bash
for (( i = 3; i <= 15; i++ ))      ### Outer for loop ###
do

    for (( j = 1 ; j <= 50; j++ )) ### Inner for loop ###
    do
        python -m referee -s 100 -t $((i * i)) $i minimax_agent random_agent >> red.txt
    done

  echo "" #### print the new line ###
done

for (( i = 3; i <= 15; i++ ))      ### Outer for loop ###
do

    for (( j = 1 ; j <= 50; j++ )) ### Inner for loop ###
    do
        python -m referee -s 100 -t $((i * i)) $i random_agent minimax_agent >> blue.txt
    done

  echo "" #### print the new line ###
done