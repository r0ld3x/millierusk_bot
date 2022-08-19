#!/usr/bin/env bash


apt-get update
apt-get upgrade



packages=("python3" "python3-pip" "virtualenv" "ca-certificates" "lsb-release" "netbase" "tzdata" "dpkg-dev" "gcc" "gnupg" "dirmngr" "libbluetooth-dev" "libbz2-dev" "libc6-dev" "libexpat1-dev" "libffi-dev" "libgdbm-dev" "liblzma-dev" "libncursesw5-dev" "libreadline-dev" "libsqlite3-dev" "libssl-dev" "make" "tk-dev" "uuid-dev" "wget" "xz-utils" "zlib1g-dev" "wget" "bash" "build-essential" "cmake" "curl" "debian-archive-keyring" "debian-keyring" "ffmpeg" "gcc" "git" "gnupg" "jq" "libatlas-base-dev" "libavcodec-dev" "libavdevice-dev" "libavfilter-dev" "libavformat-dev" "libavutil-dev" "libboost-python-dev" "libcurl4-openssl-dev" "libffi-dev" "libgconf-2-4" "libgtk-3-dev" "libjpeg-dev" "" "libopus-dev" "libopus0" "libpq-dev" "libreadline-dev" "libswresample-dev" "libswscale-dev" "libssl-dev" "libwebp-dev" "libx11-dev" "libxi6" "libxml2-dev" "libxslt1-dev" "libyaml-dev" "" "make" "mediainfo" "megatools" "meson" "musl" "musl-dev" "neofetch" "ninja-build" "openssh-client" "openssh-server" "openssl" "p7zip-full" "" "pkg-config" "procps" "python3-dev" "texinfo" "unzip" "util-linux" "wget" "wkhtmltopdf" "xvfb" "yasm" "zip" "zlib1g" "zlib1g-dev" "tesseract-ocr" "tesseract-ocr-heb" "tesseract-ocr-all" "imagemagick" "libicu-dev" "libcairo2-dev" "redis-server")



for pkg in ${packages[@]}; do

    is_pkg_installed=$(dpkg-query -W --showformat='${Status}\n' ${pkg} | grep "install ok installed")

    if [ "${is_pkg_installed}" == "install ok installed" ]; then
        echo ${pkg} is installed.
    else 
        # echo ${pkg} is not installed.
        sudo apt-get install -y ${pkg}
    fi
done

pip install --upgrade pip  && pip install --upgrade setuptools

set -e
DIR="venv"
if [ -d "$DIR" ]; then
    echo "Directory $DIR exists No Need to make venv."
else:
    echo "Directory $DIR does not exist. Making venv..."
    virtualenv venv
fi

source venv/bin/activate


if [ "$OSTYPE" == "linux*" ]; then
    pip install -r requirements.txt
    echo "Starting server..."
    python3 -m mills
else
    echo "Unknown OS Declared"
    exit 1 
fi


