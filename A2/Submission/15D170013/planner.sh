#!/bin/bash

while [[ $1 != '' ]]; do
case $1 in
    --mdp )
    shift # past argument=value
    MDP=$1
    ;;

    --algorithm )
    shift # past argument=value
    ALGORITHM=$1
    ;;
esac
shift
done

python3 extras/planner.py $MDP $ALGORITHM
