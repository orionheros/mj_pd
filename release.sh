#!/bin/bash
set -e

rsync -av --delete pd/ AppDir/usr/bin/pd/
./linuxdeploy-x86_64.AppImage --appdir AppDir \
    --plugin python \
    --desktop-file pd_ui_mng.desktop \
    --icon-file logo.png \
    --output appimage