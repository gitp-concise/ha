#!/bin/bash
python3 -m venv linux_hw
source /home/park/linux_hw/bin/activate

echo "Checking and installing required packages..."
pip install -r ./requirements.txt
if [ $? -ne 0 ]; then
    echo "pip install failed. Trying pip3..."
    pip3 install -r ./requirements.txt

    if [ $? -ne 0 ]; then
        echo "pip3 install failed. Trying pip install with --user option..."
        pip install --user -r ./requirements.txt

        if [ $? -ne 0 ]; then
            echo "All installation methods failed. Exiting."
            exit 1
        fi
    fi
fi


echo "Existing process found. Terminating..."
pkill -f check.py

echo "Starting Python script in tmux session..."
SESSION_NAME="my_first_tmux_session"
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    tmux new-session -d -s $SESSION_NAME
fi

echo "Script execution initiated in tmux session."
tmux send-keys -t $SESSION_NAME "python3 check.py" C-m

tmux attach -t $SESSION_NAME
