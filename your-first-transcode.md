# Your First Transcode

**Outcome: at least one real file,
converted by your own flow on your own
node, with the job report read and the
before-and-after numbers in hand.**
Everything before this chapter was
preparation. This is the chapter where
Tdarr does the thing.

## Giving the node its workers

Start the node beside the server:

```bash
./Tdarr_Node
```

First start creates
`configs/Tdarr_Node_Config.json` with a
generated name and the address of the
server it will look for — the same
machine, in the lab's case, at
`127.0.0.1:8266`. Within seconds the
node appears on the server's **Nodes**
page and in the API:

```bash
curl -s http://127.0.0.1:8265/api/v2/get-nodes
```

Then the trap, which the lab states as
plainly as it can because nearly
everyone meets it: **a new node has zero
workers.** Registered, connected, green
— and incapable of taking a single job.
On the Nodes page (or, as the lab did,
through the API call in transcript
`t02`), raise the counts you mean:

- **Transcode CPU: 1** — one conversion
  at a time, on the processor.
- **Health check CPU: 1** — one
  health check at a time.
- The GPU columns stay at 0: this guide
  is a CPU story until chapter 9 says
  otherwise.

One of each is the right size for a
first run on any machine: enough to see
the queue move, not enough to swamp the
box or tangle the reports together.
Worker counts are also where a node's
manners live — a node that may use one
worker overnight and four on Sundays is
a schedule away (chapter 9).

## Setting it loose

With the library scanned (chapter 4),
the flow attached (chapter 5) and a
worker waiting, the work starts itself:
the server's decision maker walks the
catalogue, queues each file for a health
check and a transcode decision, and the
node's workers pick the jobs up. The
lab triggered its scan deliberately and
the queue drained within about a
minute — its fixtures were six seconds
long; yours will take as long as your
files take.

The library's file table is the score
board. After the lab's successful run
(transcript `t04`):

```text
Cooking Basics - Episode One.avi | HC: Success |
  TDM: Transcode success | codec: h264 | size MB: 0.279
Harbour Lights - Trailer.mkv     | HC: Success |
  TDM: Transcode success | codec: h264 | size MB: 0.823
```

Two new facts per file: the health
check verdict (chapter 7) and the
transcode decision — *Transcode
success*, with the catalogue's codec and
size already updated to the new file's.
(If yours say *Error* instead, chapter
13 is written for you; the lab's first
two attempts ended there, and the
reasons were all findable in the job
reports described next.)

## Reading a job report

Pick a finished transcode on the Tdarr
page and open its report — or find the
text file the server keeps for it. A
report is long because a job is a relay:
server → node → worker, each logging its
hand-off. The lines worth finding, in
the order the lab's MKV report presents
them (transcript `t06` holds a fuller
excerpt):

```text
[Step W02] Loading flow
Creating workDir: "…/cache/tdarr-workDir2-X6mUBRO"
[Step W03] [C1] [Lab Flow - Make H.264] Running Community plugin: inputFile: Input File
…{"outputNumber":1,…}
[C2] Running Community plugin: checkVideoCodec: Check Video Codec
…{"codec": "h264"}…          <- the plugin's inputs, as loaded
…{"outputNumber":2,…}        <- output 2: not H.264 — convert
[C3] Running Community plugin: ffmpegCommandStart: Begin Command
[C4] Running Community plugin: ffmpegCommandSetVideoEncoder: Set Video Encoder
Hardware encoding is disabled in plugin input options
[C5] Running Community plugin: ffmpegCommandExecute: Execute
Running …/ffmpeg -y -i "…/Harbour Lights - Trailer.mkv"
  -map 0:0 -c:0 libx264 -crf 23 -preset veryfast
  -map 0:1 -c:1 copy  "…/cache/…"
…
File has changed, replacing original file
…destination file of size 863370 does match cache file of size 863370
Renaming original file to: …/Harbour Lights - Trailer.mkv.partial.old
Deleting renamed original file: …/Harbour Lights - Trailer.mkv.partial.old
Old size: 0.0016172714531421661
New size: 0.0008040759712457657
File processing complete
```

Read any report in that order and it
tells you the whole story: which flow,
which way each check jumped, the exact
command, where the output was built,
how the swap was verified, and the
sizes the job began and ended with. A
failed report tells the same story with
an `[-error-]` marker at the step that
broke — no other debugging tool in
Tdarr comes close, and chapter 13 is
mostly "read the report" wearing
different hats.

## What just happened, in numbers

The MKV went from 1,736,532 bytes of
MPEG-2 to 863,370 bytes of H.264 — half
the size, same name, same folder, same
six seconds of picture. The AVI went
from 721,048 bytes of MPEG-4 to 292,666
of H.264. In both, the audio stream was
copied bit for bit, because the flow
only had an opinion about video.
Chapter 8 turns those sentences into a
checking habit rather than a victory
lap: probe it yourself, outside Tdarr,
before you believe any of it.
