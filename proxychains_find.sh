SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "script dir: " $SCRIPT_DIR
python3 $SCRIPT_DIR/proxychains_find.py --chain-type=RANDOM
$SCRIPT_DIR/proxychains-ng/proxychains4 -f "/opt/homebrew/etc/proxychains.conf" $@