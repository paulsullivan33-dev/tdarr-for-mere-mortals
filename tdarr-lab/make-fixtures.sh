#!/bin/bash
# Generate the lab's fixture videos: small, invented, made by ffmpeg
# from its test patterns. Two files that break the lab's rule (video
# must be H.264) in two different ways, and one that already obeys it.
# Run in an empty folder; the folder becomes the Tdarr library.
set -e
cd "$(dirname "$0")"

# MPEG-2 video + MP2 audio in a Matroska wrapper (a "DVD-era" file)
ffmpeg -f lavfi -i testsrc2=duration=6:size=640x360:rate=25 \
       -f lavfi -i sine=frequency=440:duration=6 \
       -c:v mpeg2video -q:v 5 -c:a mp2 -shortest \
       "Harbour Lights - Trailer.mkv"

# MPEG-4 part 2 video + MP3 audio in an AVI wrapper (a "DivX-era" file)
ffmpeg -f lavfi -i testsrc2=duration=6:size=320x240:rate=25 \
       -f lavfi -i sine=frequency=660:duration=6 \
       -c:v mpeg4 -q:v 5 -c:a libmp3lame -shortest \
       "Cooking Basics - Episode One.avi"

# Already H.264 + AAC in an MP4 wrapper: the flow must leave it alone
ffmpeg -f lavfi -i testsrc2=duration=5:size=640x360:rate=25 \
       -f lavfi -i sine=frequency=880:duration=5 \
       -c:v libx264 -preset veryfast -crf 23 -c:a aac -shortest \
       "Already Compliant - Short.mp4"
