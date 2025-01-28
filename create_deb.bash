__WATCHLOG_VERSION__=$(python3 setup.py --version)

SRC=deb_dist/${__WATCHLOG_VERSION__}
DEST=~/www/bensokol.com/public/deb.bensokol.com/debian/pool/main/python3-watchlog/

GPG_KEY=1C6BFAD873C7B6D2241FEFDA2DBA02F97C909F11

echo "[sdist_dsc]" > ./setup.cfg
echo "compat: 10" >> ./setup.cfg
echo "dist-dir: ${SRC}" >> ./setup.cfg

python3 setup.py --command-packages=stdeb.command bdist_deb

debsign -k ${GPG_KEY} --re-sign ${SRC}/watchlog_${__WATCHLOG_VERSION__}-1_amd64.changes
debsign -k ${GPG_KEY} --re-sign ${SRC}/watchlog_${__WATCHLOG_VERSION__}-1_source.changes
debsign -k ${GPG_KEY} --re-sign ${SRC}/watchlog_${__WATCHLOG_VERSION__}-1.dsc

debsigs --sign=origin -k ${GPG_KEY} ${SRC}/python3-watchlog_${__WATCHLOG_VERSION__}-1_all.deb

mkdir -p ${DEST}
cp ${SRC}/*.deb  ${DEST}
cp ${SRC}/*.tar.xz ${DEST}
cp ${SRC}/*.tar.gz ${DEST}
cp ${SRC}/*.dsc ${DEST}

rm watchlog-${__WATCHLOG_VERSION__}.tar.gz
