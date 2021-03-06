# slagalica-ocr
Text recognition of the "associations" segments of the Serbian national TV quiz "Slagalica."

## How It Works
The input video file representing a specific episode of the TV quiz "Slagalica" is analyzed and the
final frames for both iterations of the "associations" game are being detected. Each of the fixed textual areas
from the final frames are processed after which they are forwarded as input to the Tesseract OCR engine.

The output is stored inside "out/cABeCDEa.txt" and "out/cABeCDEa/," where *AB* denotes the season number while *CDE*
denotes the episode number within that season. The .txt file contains the results of OCR performed
on the final frames of both iterations of the "associations" game, while the output folder contains the final frames and
each of the processed textual fields saved as images.

## User Interface & Commands
The user interface for this application is a Command-Line Interface (CLI). To interact with the application, the user must
run the Bash script "run.sh."

The following commands are supported:
* ./run.sh urls [URL] [URL...] -- downloads and analyzes episodes based on URLs supplied to the command.  
  Example: ./run.sh urls "https://www.youtube.com/watch?v=peBrEXs8SoM"
* ./run.sh sync -- retrieves the URL list of all TV Slagalica episodes. This command is required if the *all* and *random*
commands are used. Execution usually takes around 20 seconds, and the command should be executed every time there is a need
to update the URL list of episodes.
* ./run.sh random [N] -- randomly selects *N* URLs from the locally stored episode URL list obtained via the sync command
and downloads and analyzes the corresponding episodes.  
  Example: ./run.sh random 3
* ./run.sh all -- downloads and analyzes all episodes of the show based on the locally stored URL list obtained via the
sync command.
* ./run.sh local [filepath] [filepath...] -- Performs analysis of locally stored video files of the epizodes of the show. For
this command to work correctly, the local episode should be obtained by one of the commands of run.sh and the file paths should
be those of the video files stored within the local/ directory. This is because the corresponding .info.json files within the
local/ directory have the information about the season and episode numbers as well as the correct airing date. These files are
generated by the script itself upon downloading an episode.

## Dependencies
In order for this application to be runnable and useable, the following dependencies must be satisfied:
* Command-line utilities:
python3, youtube-dl, sed, jq
* Linux packages (for Ubuntu / Linux Mint):
tesseract-ocr, tesseract-ocr-srp, tesseract-ocr-srp-latn
* Python 3 libraries:
opencv-python, numpy, pytesseract, json, urllib
