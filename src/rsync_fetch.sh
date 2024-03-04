# Do not run this file directly.
# Must be used in prx python script.
SERVER=$1
WORKDIR=$2

SOURCE=$3
DEST=$4
DRYRUN=$5
REVERSE=$6

RED='\033[0;31m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
PINK='\033[0;35m'


# check if reverse sync is needed
echo "${RED}[rsync]${NC} ${PINK}Reverse sync...${NC}"
# to avoid creating a nested directory structure specify the destination directory without a trailing slash.
# e.g. rsync -azvP $DRYRUN $SERVER:$WORKDIR/${DEST}${SOURCE}/ ${SOURCE}
echo "${RED}[rsync]${NC} rrsync -azvP $DRYRUN $SERVER:$WORKDIR/${DEST}/ ${SOURCE}" 
rsync -azvP $DRYRUN $SERVER:$WORKDIR/${DEST}/ ${SOURCE}

if [ "$DRYRUN" = "--dry-run" ]; then
    echo "Dry run completed. No files were copied."  
else
    echo "completed."
fi