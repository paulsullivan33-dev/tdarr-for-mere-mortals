# Libraries and Scanning

**Outcome: a library pointing at a real
folder of media, scanned, with every
file catalogued — codecs, streams, sizes
and all — and the difference between the
two scans understood before either is
trusted.** Nothing is converted in this
chapter. Scanning only *looks*; that is
precisely why it is safe to practise on.

## What a library is

In the web interface, **Libraries → +**
creates one. Under the friendly form sit
the settings this chapter cares about:

- **Source folder** — where the media
  lives. Tdarr reads it, and (later)
  writes replacements back into it.
- **Transcode cache** — where converted
  files are built before being swapped
  in. Give it room on a fast disk: at
  any moment it may hold a second copy of
  your largest file.
- **Output folder** — empty in the lab's
  setup, and in most: an output folder
  turns the library into a converter
  (source in, results out, nothing
  replaced). This guide's main road is
  the in-place kind.
- **Scan options** — which probers run
  while cataloguing. The defaults
  (ffprobe, ExifTool and MediaInfo on;
  closed-caption scanning off) are the
  lab's too.
- **Process switches** — whether the
  library's files may be transcoded and
  health-checked at all.

The interface's default library also
arrives carrying a *classic plugin
stack* (a well-known community set for
ripping out image streams, reordering
streams and converting to MKV with
H.264/H.265) and the decision maker set
to *plugins*. Chapter 5 replaces that
with a flow; if you create your first
library in the interface and wonder why
this guide's screens differ, that is
why. The lab's library document —
created through the API from the
interface's own template so every field
could be written down — is kept at
`tdarr-lab/library.json`, with the
handful of changed fields listed in
transcript `t03`.

## What scanning records

A scan walks the folder and probes every
file it finds with ffprobe, ExifTool and
MediaInfo. For the lab's AVI fixture,
the catalogue entry afterwards reads
(trimmed):

```json
{
  "file": "/…/media/Cooking Basics - Episode One.avi",
  "container": "avi",
  "video_codec_name": "mpeg4",
  "audio_codec_name": "mp3",
  "video_resolution": "480p",
  "file_size": 0.6876449584960938,
  "duration": 6,
  "scannerReads": { "ffProbeRead": "success" }
}
```

Size in megabytes, each stream's codec,
the works — plus two verdict fields that
later chapters live in: `HealthCheck`
and `TranscodeDecisionMaker`, which fill
in as jobs run. Notice what the probe
establishes for free: this file's video
is MPEG-4 part 2, which is *not* the
H.264 the lab's standard will demand.
No conversion has happened; the scanner
has simply taken the library's
temperature, file by file.

## The two scans

**Scan (Find new)** is the everyday one.
It probes files the catalogue does not
know, and files whose on-disk state has
changed behind Tdarr's back. Files it
already knows, in the state it left
them, are passed over quickly. After a
file is converted and replaced *by
Tdarr*, its catalogue entry is updated
to match — so a Find new scan right
after a successful run finds nothing to
do, which chapter 8 treats as a feature
and a proof.

**Scan (Fresh)** discards the library's
catalogue and probes everything again
from nothing. It is the honest reset —
and the expensive one on a big library,
because thousands of files must be
probed before any work can start. Reach
for it when the catalogue and the disk
have genuinely parted company (a bulk
rename done outside Tdarr, a restored
backup), not as a way to make Tdarr
"try again": for that, the file tables
on the library page let you requeue
individual files.

A third option, **folder watching**,
removes the button-pressing: Tdarr
notices changes in the folder (by
watching file-system events, or polling
at an interval you set) and scans what
changed. The lab did not enable it —
its scans were deliberate, one variable
at a time — and it is described here so
the switch is not a surprise. On a real
library it is the difference between a
chore and a standing order, and it is
how chapter 1's promise ("new arrivals,
held to the standard") is actually kept.

## The check

After the lab's first scan the file
table showed both fixtures, with their
codecs named and both verdict columns
already filling (chapter 6 explains why
jobs ran so quickly). Your equivalent
check, on any library: the file count
matches the folder, and every file
shows a video codec you recognise as
its true one. If a file's probe failed,
its `scannerReads` say which prober
failed — that is a file problem or a
missing tool, and the library page
surfaces it rather than guessing.
