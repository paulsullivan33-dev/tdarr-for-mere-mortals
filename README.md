# Tdarr for Mere Mortals

A media library drifts. Files arrive over
years, from different sources, in
different shapes: an MPEG-2 recording
here, an old AVI there, one file with
three audio tracks nobody needs, another
that will not play on the television at
all. Tidying that by hand means running
a converter over every file yourself —
and remembering to do it again for every
new arrival. **Tdarr** is the tidy-up,
automated and distributed: you state the
standard your library should meet, and
Tdarr checks every file against it,
converting the ones that fall short and
leaving the ones that pass completely
alone.

It is two programs. A **server** keeps
the catalogue, the rules and the queue,
and serves a web interface. **Nodes** —
small workers you run on any machine
with spare hours, including the same
one — take files from the queue, check
them, and convert the ones that need it
with **ffmpeg** or **HandBrake**. The
rules are **flows**: little chains of
checks and actions you assemble from
plugins, most of them written by the
community. "Every video in this library
shall be H.264" is a flow. So is "strip
the commentary tracks" and "nothing
above 1080p".

The lab behind this guide ran the real
thing: **Tdarr 3.04.00**, installed from
the project's own distribution on a
small Linux machine, one server and one
node on the same box, talking over
loopback. It made three tiny fixture
videos with ffmpeg — an MPEG-2 file, an
MPEG-4 AVI, and one file already in
H.264 — pointed a library at them, built
a flow that re-encodes anything that is
not H.264, and watched the node convert
the two offenders end to end: sizes,
codecs and job reports all recorded.
The compliant file went through the same
flow and came out untouched, with the
verdict *Not required*.

The lab also failed, informatively, and
those failures are kept, because they
are the ones you will meet: a node that
could not reach its own server, a plugin
library installed one folder short —
twice — and health checks that insisted
on a HandBrake program the machine did
not have.

What the lab could not do, it did not
fake. There is no graphics card in the
sandbox, so hardware encoding is
explained but switched off in every lab
flow and never benchmarked. Nodes on
*other* machines, the Docker install,
and the classic plugin stacks are taught
from the documentation and labelled as
such wherever they appear. `criteria.md`
keeps the full ledger of what was run
and what was only read.

## What this guide covers

- [**What Tdarr is**](what-tdarr-is.md) —
  the mental model: a standard for your
  library, a server that keeps score,
  and workers that bring files up to it
- [**The moving parts**](the-moving-parts.md) —
  the server, the nodes and their
  workers, libraries, flows and plugins,
  the transcode cache and the staging
  area — and which part holds what
- [**Installing Tdarr**](installing-tdarr.md) —
  the Updater and the direct packages,
  the first start, the start-up
  self-tests, ports, and the sign-in
  you should leave switched on
- [**Libraries and scanning**](libraries-and-scanning.md) —
  telling Tdarr where your files live,
  what a scan actually records, and the
  difference between finding new files
  and starting fresh
- [**Your first flow**](your-first-flow.md) —
  the H.264 flow from the lab, plugin by
  plugin: a check with two exits, an
  encoder chain, and the careful
  replacement at the end
- [**Your first transcode**](your-first-transcode.md) —
  giving a node its workers, watching a
  job through the queue, and reading the
  job report that proves what ran
- [**Health checks**](health-checks.md) —
  the second kind of job: probing files
  for damage, quick and thorough modes,
  and choosing ffmpeg or HandBrake for
  the work
- [**Proving the transcode**](proving-the-transcode.md) —
  before-and-after probes, sizes, the
  verdicts a file can carry, and why a
  second scan finds nothing to do
- [**Nodes and workers**](nodes-and-workers.md) —
  more machines on the same queue,
  worker types and limits, schedules,
  and the path translators that let a
  Windows node serve a Linux server
- [**Recipes**](recipes.md) — make
  everything AAC, cap a library at
  1080p, strip unwanted streams, keep a
  copy instead of replacing, and the
  classic plugin stack the templates
  still offer
- [**The neighbours**](the-neighbours.md) —
  HandBrake on its own, a folder of
  ffmpeg scripts, FileFlows and Unmanic:
  what each does that Tdarr doesn't, and
  vice versa
- [**Limits**](limits.md) — replacement
  is destructive, a flow is only as good
  as its plugins, one decision maker per
  library, no playback or library
  browsing, and the honest price of
  "free"
- [**Troubleshooting**](troubleshooting.md) —
  the node that posts its handshake to a
  proxy, workers stuck at zero, the two
  missing plugin folders, the absent
  HandBrake, and the traps this guide's
  lab fell into
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Playing or organising media: Tdarr
converts files, it is not a media
server — the Jellyfin guide in this
series is the serving half. Where the
files come from is likewise out of
scope; this guide starts with files you
already have and ends with the same
files, standardised. GPU encoding is
explained and honestly labelled
unmeasured. And nothing here touches
anyone else's library: flows run on
folders you point them at, and chapter
12 is plain about how much damage a
careless flow can do to your own.

## How to use this guide

Read chapter 1 for the model and
chapter 2 before installing anything —
most confusion with Tdarr is two parts
being mistaken for each other, and
chapter 2 names them all. Chapters 3
and 4 get you a server and a scanned
library; chapters 5 and 6 build the
flow and watch it work, in the same
sitting. Chapter 8 is the one to read
slowly: its checks are how you know a
conversion really happened — and really
needed to — before you let a flow loose
on a library you care about. The lab's
transcripts live in `tdarr-lab/transcripts/`;
its flow and library documents are
`tdarr-lab/lab-flow.json` and
`tdarr-lab/library.json`, its fixture
generator is `tdarr-lab/make-fixtures.sh`,
and the script that created the flow and
library through the API is
`tdarr-lab/make-flow-library.py`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [HandBrake for Mere Mortals](https://paulsullivan33-dev.github.io/handbrake-for-mere-mortals/)
- [ffmpeg for Mere Mortals](https://paulsullivan33-dev.github.io/ffmpeg-for-mere-mortals/)
- [Jellyfin for Mere Mortals](https://paulsullivan33-dev.github.io/jellyfin-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/tdarr-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/tdarr-for-mere-mortals/blob/main/LICENSE-CODE).
