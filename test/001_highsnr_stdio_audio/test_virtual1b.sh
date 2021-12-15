#!/bin/bash -x
# Run a test using the virtual sound cards, tx sound I/O performed by Python,
# rx using arecord, Fs=48000Hz

function check_alsa_loopback {
    lsmod | grep snd_aloop >> /dev/null
    if [ $? -eq 1 ]; then
      echo "ALSA loopback device not present.  Please install with:"
      echo
      echo "  sudo modprobe snd-aloop index=1,2 enable=1,1 pcm_substreams=1,1 id=CHAT1,CHAT2"
      exit 1
    fi  
}

check_alsa_loopback

RX_LOG=$(mktemp)
MAX_RUN_TIME=2600

# make sure all child processes are killed when we exit
trap 'jobs -p | xargs -r kill' EXIT

arecord -r 48000 --device="plughw:CARD=CHAT1,DEV=0" -f S16_LE -d $MAX_RUN_TIME | \
    sox -t .s16 -r 48000 -c 1 - -t .s16 -r 8000 -c 1 - | \
    python3 test_rx.py --mode datac0 --frames 2 --bursts 5 --debug &
rx_pid=$!
sleep 1
python3 test_tx.py --mode datac0 --frames 2 --bursts 5 --delay 500 --audiodev -2
wait ${rx_pid}