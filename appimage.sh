#!/bin/bash
set -e

export PYTHON__VERSION=3.12.3
export PYTHON_EXECUTABLE=/usr/bin/python3.12
export PIP_REQUIREMENTS_FILE=requirements_linux.txt
export PYTHON_ENTRYPOINT="pd/__main__.py"
export QMAKE=/usr/bin/qmake6

mkdir -p AppDir/usr/bin

cp -r pd AppDir/usr/bin/pd

cp pd/__main__.py AppDir/usr/bin/mj_pd
chmod +x AppDir/usr/bin/mj_pd

./linuxdeploy-x86_64.AppImage --appdir AppDir \
    --plugin python \
    --desktop-file pd_ui_mng.desktop \
    --icon-file logo.png \
    --output appimage