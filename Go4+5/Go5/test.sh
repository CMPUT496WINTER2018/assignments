#!/bin/bash

python3 Go5.py --movefilter --in_tree_knowledge="probabilistic" --num_total_sim=1 << EOF
    
boardsize 3
play b b2
play w a2
play b b3
play w a3
prior_knowledge

EOF
   

