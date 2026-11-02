# Health Checks

**Outcome: a clear picture of Tdarr's
second kind of job — the health check —
what its verdicts mean, which tool does
the checking, and why your library's
health-check setting may name a program
you do not have.** Every file the lab
converted was health-checked twice:
once on the way in, once on its new
self on the way out. Both passed. This
chapter is about the times one would
not.

## What a health check is

A health check asks a simpler question
than a transcode: *is this file
intact?* Not "is it the right codec" —
that is the flow's business — but "does
it decode, start to finish, without
errors". A truncated download, a copy
interrupted halfway, a disk quietly
going bad: all of them leave files that
look fine in a listing and fall over
four minutes into the film. The health
check is Tdarr walking the file before
your television does.

There are two depths:

- **Quick** checks read the file's
  structure and a sample of its content
  — fast, and enough to catch files that
  are plainly broken or incomplete.
- **Thorough** checks decode the whole
  file with the converter, which takes
  about as long as playing it would on a
  slow machine, and catch damage hiding
  in the middle.

The verdict lands in the catalogue
beside the transcode decision:
**Success**, or **Error** — and an
Error verdict keeps the file out of the
transcode queue until a human looks,
because converting a damaged file
mostly manufactures a damaged file in a
newer codec.

## Which tool does the checking

Here the lab hands you its most
transferable lesson. Health checks are
run by an external converter, and the
library chooses which: a per-library
setting in the template the interface
starts from defaults to **HandBrake**
(`handbrakescan`), with ffmpeg the
alternative (`ffmpegscan`). HandBrakeCLI
is not part of Tdarr's download. On the
lab's machine it was not installed at
all, and every health check of the
first two attempts died in under four
seconds with this in its job report
(transcript `t04`):

```text
Subworker: Error executing binary: HandBrakeCLI
  No such file or directory (os error 2)
```

Two honest ways out, and the guide
takes the second:

1. **Install HandBrakeCLI** — the
   HandBrake project's own CLI build,
   from their site or your distribution.
   Tdarr's start-up tests then find it,
   and the defaults stand as shipped.
2. **Switch the library to ffmpeg:**
   in the library's settings, turn off
   HandBrake scanning and turn on ffmpeg
   scanning. The checker becomes the
   ffmpeg Tdarr already bundles — the
   same engine the flows use — and no
   new program enters the machine.

What you may not do is mistake the
start-up line *Binary test 1:
handbrakePath not working* for a broken
install (chapter 3): it is a report
that an optional companion is absent,
and with the library switched to ffmpeg
it has nothing left to affect.

## Health checks around a transcode

The sequence the lab observed, and the
one to expect: a newly scanned file is
health-checked *before* its transcode
decision is acted on, and a file that
was just replaced by a transcode is
health-checked *again* on its new
version — the MKV's record shows two
Success health checks bracketing its
one transcode (transcript `t04`). That
second check is Tdarr proving its own
work before calling it done, and it is
the right shape for a tool whose
failures are otherwise silent until
playback.

## The check

On any library, read the health column
as a triage list, not a grade. All
Success: the library is whole, as far
as decoding can tell. One Error: open
that file's job report, read which tool
ran and where it stopped — a check that
failed because its *tool* was missing
looks exactly like a broken file until
the report's last lines separate them
(the lab's HandBrake reports are the
worked example). Many Errors at once,
on files that used to pass: stop
transcoding, suspect the disk or the
copy that made them, and let chapter 13
walk you through it in that order.
