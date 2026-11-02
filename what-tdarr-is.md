# What Tdarr Is

You have a folder of video files — a
library — and it is not in the shape you
would choose. Some files are enormous
for what they hold, because they were
recorded in an old, inefficient format.
Some will not play on a picky device.
Some carry audio tracks, subtitles or
commentary you never asked for. None of
this stops you watching them, exactly;
it just nags, file by file, year by
year.

You could fix each file by hand with a
converter (chapter 11's neighbours do
exactly that, well). What you cannot do
by hand is fix *every future file the
same way* — the new arrival next month
will be just as odd as the last one,
because you did not make it either.

**Tdarr is a standing order for a
library.** You declare the standard —
say, *video in H.264, audio in AAC,
nothing above 1080p* — and Tdarr holds
every file in the library up against
it, now and as new files arrive. Files
that meet the standard are left strictly
alone. Files that fall short are queued,
converted on whatever machines you give
it, checked again, and put back in
place. The name is short for
*transcode arranger*, in the family of
library-keeping tools whose names end
in *-arr*.

The work splits across two programs,
because the thinking and the lifting are
different jobs:

- The **server** keeps the catalogue
  (what every file is, down to each
  stream), the rules (your standard,
  expressed as a **flow**), and the
  queue of work. It serves the web
  interface you manage it all from.
- **Nodes** do the lifting. A node is a
  small program that connects to the
  server, asks for work, and runs the
  checks and conversions with the
  converter tools on its machine. Run
  one on the server's own machine, or on
  every idle computer in the house: the
  queue does not care.

The lab that wrote this guide ran both
on one small machine. It told Tdarr:
*this folder is a library; the standard
is "video is H.264"; the cache is over
there.* Then it watched. One MPEG-2 file
came back half its former size wearing
H.264. One old AVI likewise. One file
that already met the standard was
probed, judged *Not required*, and not
touched at all. Those three verdicts —
converted, converted, left alone — are
the whole tool in miniature, and
transcript `t04` and `t05` in the lab
folder keep the receipts.

## A first taste

Nothing about Tdarr happens at a command
line in normal use — it happens in the
web interface, at `http://<server>:8265`.
But the server's own API answers the
question "are you alive, and which
version are you" to anyone who asks,
which makes a fine first check after
installing (chapter 3):

```bash
curl -s http://127.0.0.1:8265/api/v2/status
```

```json
{"status":"good","isProduction":true,"os":"linux","version":"3.04.00","buildDate":"2026_10_27T16_56_14z","uptime":36,"serverEngine":"rust"}
```

That is Tdarr **3.04.00**, the version
this guide's lab installed and used
throughout.

## What it is not

Tdarr is not a media server: nothing in
it plays a file, shows a poster, or
knows what a television is. It prepares
files *for* players; the Jellyfin guide
in this series covers the playing. It
is not a downloader or a library
manager: it does not fetch, name, or
organise your collection (the Sonarr
and Radarr guide covers that family).
It is not, despite appearances, a video
editor or a converter with opinions of
its own: every decision it makes is a
plugin in a flow you assembled, and
chapter 12 is plain about what that
means when the flow is wrong. And it is
not gentle by default — a flow that ends
in "replace the original" really does
replace the original, which is why
chapter 8 (proving the result before
trusting the process) exists.

## Who it is for

The home media keeper whose library has
outgrown hand-conversion — hundreds of
files, several sources, one television
with strong opinions about codecs. The
owner of spare machines: a media PC, an
old desktop, a home server with idle
evenings, all of which can be nodes.
The recorder of broadcast television,
whose files arrive in whatever format
the tuner chose. The common thread is a
library big enough that "I'll convert
it when I notice" has quietly stopped
being true.

## The honest catch, up front

Tdarr's power and its danger are the
same sentence: *it will do exactly what
the flow says, to every file in the
library, unattended.* A good flow is a
tireless librarian. A sloppy flow is a
tireless vandal, and the originals it
replaces are gone in a way no undo
button covers. This guide therefore
builds its first flow small, tests it on
fixtures made to be thrown away, and
only then talks about real libraries.
Start where the lab started.
