# Proving the Transcode

**Outcome: a checking routine — probe,
size, verdict, second scan — that lets
you believe a conversion happened,
needed to happen, and will not happen
again, using tools outside Tdarr as the
witnesses.** A transcode program that
fails quietly still writes files, and a
flow that misfires writes them at
library scale. This chapter is the
habit that catches both early.

## Probe it yourself

Tdarr's catalogue is a claim. `ffprobe`
is the audit. For every converted file,
in the lab and in this chapter, the same
two facts were taken from the file
itself, before and after — the stream
codecs and the byte size (transcripts
`t01` and `t04` hold both rounds):

```bash
ffprobe -v error \
  -show_entries stream=codec_type,codec_name \
  -show_entries format=size -of compact "<file>"
```

The lab's evidence, side by side:

| File | Before | After |
| --- | --- | --- |
| Harbour Lights - Trailer.mkv | mpeg2video + mp2, 1,736,532 bytes | h264 + mp2, 863,370 bytes |
| Cooking Basics - Episode One.avi | mpeg4 + mp3, 721,048 bytes | h264 + mp3, 292,666 bytes |
| Already Compliant - Short.mp4 | h264 + aac, 483,259 bytes | h264 + aac, 483,259 bytes |

Read the table the way an auditor
would. The video codec changed to the
standard, exactly where the standard
was unmet. The audio codec did *not*
change anywhere — the flow had no
opinion about audio, and a correct run
leaves what it has no opinion about
alone; if your table shows audio
converted too, your flow said so
somewhere, or a plugin you did not
notice did. The sizes fell by half and
by 59%, which is the *characteristic*
shape of MPEG-2 and MPEG-4 part 2 being
retired for H.264 at a sane quality —
treat dramatically *larger* outputs, or
outputs within a whisker of the input
size, as questions, not results. And
the compliant row is byte-identical in
every column: the flow recognised it,
and restrained itself.

## Know the verdicts

A file's transcode decision, as the
catalogue records it, has a small
vocabulary, and each word is a
different state of the world:

- **Transcode success** — the flow ran,
  produced a new file, and (with
  staging approval or auto-accept) the
  swap was made and verified.
- **Not required** — the flow ran and
  the file fell out of a check's passing
  exit. Nothing was built, nothing was
  touched. This is a *success* state —
  on a healthy library, it is the most
  common one.
- **Transcode error** — the flow ran and
  something in it failed: a missing
  plugin folder, a converter that would
  not start, an output the checks
  rejected. The job report names the
  step.
- **Queued / in progress** — the honest
  middle states; a file that lives here
  for hours is a worker problem
  (chapter 9), not a flow problem.

Health check verdicts sit beside these
(chapter 7): Success, or Error with the
report to explain it. A file whose
transcode says success but whose
post-transcode health check says Error
is the one combination that should stop
your day: Tdarr made a file its own
checker distrusts, and the original it
replaced is gone. It did not happen in
the lab. The staging habit in chapter 2
is what makes it survivable if it ever
happens to you.

## The second scan

The last proof is a non-event. Run
**Scan (Find new)** again on a library
whose files all carry verdicts
(transcript `t05`):

```text
…no new jobs at all. The job table
afterwards is identical.
```

Tdarr replaced those files itself and
wrote their new state into the
catalogue as it went; nothing on disk
disagrees with anything it knows, so
there is nothing new to find. That is
what "done" looks like in this tool —
not a fanfare, but a scan that shrugs.
If your second scan *does* requeue
everything, one of three things is
true: the files changed outside Tdarr
(another program is rewriting them),
the catalogue and the disk disagree
(chapter 4's Fresh scan is the reset),
or the flow's standard and the flow's
output disagree — a flow that demands
H.264 but writes H.265 will convert its
own output forever, and the second scan
is exactly how you catch it before it
has eaten the library twice.
