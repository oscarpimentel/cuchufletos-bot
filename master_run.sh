#!/bin/bash
reset
SECONDS=0
run_python_script(){
	now=$(date +"%T")
	echo -e "\e[7mrunning script ($now)\e[27m python $1"
	eval "python $1"  # to perform serial runs
	# eval "python $1 > /dev/null 2>&1" & # to perform parallel runs
}
intexit(){
    kill -HUP -$$
}
hupexit(){
    echo
    echo "Interrupted"
    exit
}
trap hupexit HUP
trap intexit INT
echo -e "\e[7mrunning master_run... (ctrl+c to interrupt)\e[27m $1"
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
run_python_script "run_bot.py --debug"
run_python_script "run_bot.py"
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
mins=$((SECONDS/60))
echo -e "\e[7mtime elapsed=${mins}[mins]\e[27m"