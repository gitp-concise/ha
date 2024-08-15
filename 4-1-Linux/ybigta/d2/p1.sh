#!/bin/sh

session_name="YBIGTA"
py_version="3.9"

# create virtual environment
pipenv --python ${py_version}

# install package 
echo "Checking and installing required packages..."
pipenv install -r requirements.txt &> /dev/null

# kill check.py process if running
py_pids=$(ps aux | grep -v "grep" | grep "python check.py" | awk '{print $2}')
if  [[ ${py_pids} =~ [0-9]+ ]]; then
	echo "Existing process found. Terminating..."
	echo ${py_pids} | xargs kill -9 
fi


# check if session name of ${session_name} exists
echo "Starting Python script in tmux session..."
if ! ( tmux ls | grep -q "^${session_name}:" ); then
	tmux new-session -d -s ${session_name} 
fi

tmux send-keys -t ${session_name} "pipenv run python check.py" C-m

echo "Script execution initiated in tmux session..."
tmux a -t ${session_name}
