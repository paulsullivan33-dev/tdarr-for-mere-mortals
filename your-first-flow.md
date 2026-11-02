# Your First Flow

**Outcome: a saved flow that states one
rule of your standard — *video shall be
H.264* — with a door for files that pass
and a conversion for files that fail.
It converts nothing yet; chapter 6 sets
it loose. The lab built this exact flow
(transcript `t03`); the interface's
**Flows** page builds it by dragging,
and a tutorial template set ships with
the plugin library for company.

## The shape of a flow

A flow is a chain of plugins wired
output to input, read top to bottom.
Every flow starts with the same plugin —
**Input File** — which hands the file
from the queue to the next plugin. Every
plugin answers by choosing one of its
numbered **outputs**, and the wire from
that output decides where the file goes
next. The flow ends wherever the wires
run out: a file that reaches the end of
its wire is done, with whatever the last
plugins did to it standing as the
result.

The lab's flow, with the plugin names as
the library gives them:

```text
Input File
   │
   ▼
Check Video Codec        input: codec = "h264"
   ├── output 1 "file has codec" ──────► (end — untouched)
   └── output 2 "does not have it" ──► Begin Command
                                          │
                                          ▼
                                       Set Video Encoder
                                          │
                                          ▼
                                       Execute
                                          │
                                          ▼
                                       Replace Original File
```

Six plugins, one idea. Take them in
turns.

## The check: Check Video Codec

Community plugin `checkVideoCodec`. It
reads the catalogue record (chapter 4)
rather than the disk, which is why a
flow runs fast even over a huge library.
It has exactly one input — the codec to
test for — and two outputs: **1**,
*file has codec*, and **2**, *file does
not have codec*. The lab set the input
to `h264` and wired output 1 to nowhere
at all. That bare wire is the most
important idea in this guide: **a flow
only touches the files its wires lead
somewhere.** Files that pass simply fall
out of the flow, unconverted, at the
cost of one catalogue lookup — chapter 8
watches one do exactly that and collect
the verdict *Not required*.

## The command chain: three plugins, one command

Transcoding with ffmpeg inside a flow is
a three-plugin sentence:

- **Begin Command** (`ffmpegCommandStart`)
  opens an empty ffmpeg command for this
  file, with every stream set to *copy*
  by default.
- **Set Video Encoder**
  (`ffmpegCommandSetVideoEncoder`) changes
  the video stream's order from *copy* to
  *encode*. Its inputs are the ones that
  decide your library's future, and the
  lab set them deliberately:
  - `outputCodec`: `h264` (the plugin's
    default is `hevc` — check this input
    first, always)
  - `ffmpegPreset`: `veryfast` (how much
    time the encoder spends squeezing;
    slower presets make smaller files,
    not better-looking ones at the same
    quality setting)
  - `ffmpegQuality`: `23` (the constant
    quality target — lower is better
    looking and bigger; 23 is the
    encoder's own middle)
  - `hardwareEncoding` / `hardwareDecoding`:
    **off**. Both default to *on*, with
    the type on *auto* — on a machine
    with a suitable GPU that is free
    speed; on the lab's GPU-less box it
    would have sent the job hunting for
    hardware that is not there. This
    guide's rule: hardware off until you
    have watched CPU encoding succeed,
    then on as its own experiment
    (chapter 10 has the recipe-shaped
    version of that advice).
- **Execute** (`ffmpegCommandExecute`)
  runs the built command — in the cache
  folder, never over the original — and
  passes the new file down the wire.

The command those three produced for
the lab's MKV file is worth reading
once, slowly, because it is the whole
flow with the wrapping off (from the
job report, transcript `t06`):

```text
ffmpeg -y -i "Harbour Lights - Trailer.mkv"
  -map 0:0 -c:0 libx264 -crf 23 -preset veryfast
  -map 0:1 -c:1 copy
  "<cache>/Harbour Lights - Trailer.mkv"
```

Stream 0 (video) is re-encoded with the
H.264 encoder at quality 23, preset
veryfast. Stream 1 (audio) is `copy` —
untouched, as Begin Command left it,
because no plugin in the chain said
otherwise. If you read the ffmpeg guide
in this series, nothing here is magic;
if you do not, trust the job report to
show you this line for every file, and
read it before you scale up.

## The ending: Replace Original File

Community plugin `replaceOriginalFile`.
It takes the working file the flow
produced and swaps it for the original
— carefully, as chapter 6's report
excerpt shows: copied beside the
original under a temporary name, size
checked against the cache copy, the
original renamed aside, the new file
moved into its name, and only then the
old one deleted. If the flow produced
*nothing new* for a file, this plugin
leaves the original standing.

The alternative endings matter for
chapter 10: **Move To Directory** keeps
the result and sends it elsewhere
(folder-to-folder conversion), and doing
nothing at all leaves the converted
file in the cache and the original in
place, for flows that are only
*measuring*. Replace is the ending that
makes Tdarr a standing order rather
than a report, and the one that earns
chapter 12's warning.

## Attaching the flow to the library

A flow does nothing until a library
points at it. In the library's
transcoding settings, the **decision
maker** chooses *what judges files*:
the classic plugin stack, the basic
video/audio settings, or **Flows** —
and, for flows, which one. The lab's
library sets exactly that
(`decisionMaker.settingsFlows`, and a
`flowId`), listed field by field in
transcript `t03`. One library, one
decision maker: you cannot run two
flows over the same file and merge the
verdicts, which chapter 12 counts as a
real limit and chapter 10 works around
with *Go To Flow* chains for readers
who outgrow one chain.

## The check

Save the flow and open it again: six
plugins, the codec input reads `h264`,
output 1 of the check is unwired,
output 2 reaches Replace Original File
in four hops, and the library's
decision maker names this flow. If any
plugin shows the encoder defaulting to
`hevc`, you have found the one input
that silently changes the whole guide's
outcome — fix it now, while the only
thing at stake is a diagram.
