@echo off

set BIN_NAME=sqlitebiter

echo "----- start -----"
python make_result_matrix.py -o pages\reference --type reference
echo "----- complete -----"


echo "----- start compress -----"
set DIST_DIR_NAME=dist
set BIN_PATH=%DIST_DIR_NAME%/%BIN_NAME%
set ARCHIVE_PATH=%DIST_DIR_NAME%/%BIN_NAME%_win_x64

pause