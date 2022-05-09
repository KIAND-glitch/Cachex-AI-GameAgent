#!/bin/bash
echo "RED" >> results.txt

for (( i = 3; i <= 15; i++ ))      ### Outer for loop ###
do
    echo "size $i" >> results.txt
    for (( j = 1 ; j <= 50; j++ )) ### Inner for loop ###
    do
        python -m referee -s 100 -t $((i * i)) -l log.txt $i minimax_agent_v2 random_agent
        tail -n 1 log.txt >> results.txt
    done

done

echo "" >> results.txt
echo "BLUE" >> results.txt

for (( i = 3; i <= 15; i++ ))      ### Outer for loop ###
do
    echo "size $i" >> results.txt
    for (( j = 1 ; j <= 50; j++ )) ### Inner for loop ###
    do
        python -m referee -s 100 -t $((i * i)) -l log.txt $i random_agent minimax_agent_v2
        tail -n 1 log.txt >> results.txt
    done


done