# copy all files from the spidercam_simulator directory to the destination directory and remove emojis
# usage: ./remove_emojis.sh <destination directory>
# if no destination directory is provided, the directory ../tex/code is used
if [ -z "$1" ]
then
    DEST=../tex/code
else
    DEST=$1
fi

# copy all files from the spidercam_simulator directory to the destination directory
cp spidercam_simulator/*.py $DEST

# remove all non-utf8 characters from the copied files (like 🎮)
for file in $DEST/*.py
do
    perl -i -pe 's/[^[:ascii:]]//g' $file
done
