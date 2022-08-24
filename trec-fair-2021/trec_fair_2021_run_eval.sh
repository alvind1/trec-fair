#!/bin/sh

# Assuming we are in the wptrec conda environment

#arg 1 should be eval-folder
#args 2 ... should be run files

if [ -z "$1" ]; then
    echo "eval folder can't be empty"
    exit 1
fi

if [ -z "$2" ]; then
    echo "queries type must either be train or eval"
    exit 1
fi

if [ -z "$3" ]; then
    echo "run files can't be empty"
    exit 1
fi

curr_dir=$(pwd)
eval_folder=$1
shift
query_type=$1
shift
rm -f $eval_folder/runs/*
cp "$@" "$eval_folder/runs/"
gzip $eval_folder/runs/*
ls $eval_folder/runs/*
cd "$eval_folder"
python Task1Evaluation.py --$query_type
cp results/* $curr_dir/results/
