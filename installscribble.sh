echo Welcome to Whale64 SuperInstall v1
echo Here are some things you should know:
echo 1: Do not close this window until you are told to do so.
echo 2: Seeing lots of random text is completely normal. Do not be alarmed.
echo 3: You are about to install: ScribbleNotes.
sleep 2

while true; do
    read -p "Are you ready to install the program?  (y = yes) (n = no)" yn
    case $yn in
        [Yy]* ) bash <(wget -qO- https://whale64.net/scribble.sh);;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

