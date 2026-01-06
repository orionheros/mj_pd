#!/bin/bash
set -e

APP_NAME="PD UI Mng"
VERSION="0.2.0"
ARCH="amd64"

pyinstaller --clean pd.spec

mkdir -p pkg/DEBIAN
mkdir -p pkg/usr/local/bin
mkdir -p pkg/usr/share/applications
mkdir -p pkg/usr/share/icons/hicolor/256x256/apps

cp dist/pd-ui-mng pkg/usr/local/bin/pd-ui-mng
cp assets/pd-ui-mng.desktop pkg/usr/share/applications/
cp assets/icon.png pkg/usr/share/icons/hicolor/256x256/apps/pd-ui-mng.png

cat > pkg/DEBIAN/control << EOF
Package: pd-ui-mng
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Depends: libc6, libgl1, libxcb1
Maintainer: Mateusz Jamróz
Description: PD UI Mng
EOF

dpkg-deb --build pkg ${APP_NAME}_${VERSION}_${ARCH}.deb
