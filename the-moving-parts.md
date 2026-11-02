# The Moving Parts

Tdarr looks like one program with a web
page. It is better understood as eight
parts doing eight jobs, because nearly
every surprise in this guide — including
most of the troubleshooting chapter —
is one part behaving exactly as designed
while the reader expected another part's
behaviour. This chapter names them.

## The server

The server is the brain and the only
part that must always be running. It
holds the catalogue of every scanned
file (each file's streams, codecs,
sizes and verdicts), the libraries, the
flows, and the work queue. It serves
the web interface and the API on port
**8265**, and accepts node connections
on port **8266**. Its data lives in a
folder it creates beside itself —
settings in `configs/`, and under
`server/Tdarr/` its database folders,
plugins, logs and backups. If the
server stops, nothing is lost; if its
data folder is lost, everything it knew
is.

## Nodes and workers

A **node** is the muscle: a small
program that connects to the server and
asks, every couple of seconds, "anything
for me?" A node carries no rules of its
own beyond where the server is and how
its machine's paths line up with the
server's (chapter 9's path translators).

Inside a node, the unit of capacity is
the **worker**. Workers come in four
kinds — transcode and health check,
each on CPU or GPU — and a node starts
with **zero of all of them**. This is
the single most common first-day
puzzle: a perfectly healthy node,
registered and green in the interface,
that never takes a job, because nobody
gave it any workers. Chapter 6 gives it
some. A node's name is random poetry
(the lab's called itself *good-gar*,
and its workers *pink-pig*, *odd-olm*
and *zany-zeren*); you can rename it,
and should once you have several.

## Libraries

A **library** is a folder, plus
settings: where the media is, where the
transcode cache is, which checks to run
while scanning, and which decision maker
judges its files. Libraries are the
unit of policy — different folders can
live by different standards. A film
library might demand H.264 and AAC; a
home-video library might only demand
"plays everywhere" and keep its odd
audio as it is.

## The catalogue and the scanner

When a library is scanned, Tdarr probes
every file with ffprobe, ExifTool and
MediaInfo and writes down what it finds:
container, each stream's codec and size,
resolution, duration, and the rest. That
record *is* the file, as far as every
later decision is concerned — flows read
the catalogue, not the disk. Two scan
modes matter: **Scan (Find new)** adds
files it has not catalogued (or whose
disk state has changed without Tdarr
knowing), and **Scan (Fresh)** throws
the catalogue for the library away and
starts again. Chapter 4 uses both, and
chapter 8 shows Find new deliberately
finding nothing after a successful run.

## Flows and plugins

A **flow** is the standard, made
executable: a chain of **plugins**, each
one a check or an action, wired output
to input. A check plugin has several
exits — *file has codec 1*, *file does
not have codec 2* — and the wiring
decides what happens down each road. An
action plugin does something: builds an
ffmpeg command, runs it, moves a file,
replaces the original. Plugins live in
two families: **community** plugins,
written and shared by other users (the
lab used five of them), and **local**
ones you write yourself. An older way of
working — the **classic plugin stack**,
an ordered list instead of a wired
chain — still exists, and the default
library template still carries one
(chapter 10); flows are the present and
the future, and this guide's main road.

## The transcode cache

No plugin ever writes over your file
directly. Conversions happen in the
library's **transcode cache** folder: the
node builds the new file there, Tdarr
probes it, compares it, and only then
does the flow's final step swap it into
place — copy beside the original,
verify the size, rename the original
aside, move the new one in, delete the
old. Chapter 6 reads that choreography
out of a real job report. A fast, roomy
cache folder is not a luxury; it is
where your library's second copy
temporarily lives.

## The staging area

Between "converted" and "kept" sits the
**staging area**. By default, a finished
transcode waits there for a human to
accept it — the original untouched until
you say so. That is the safe setting
while a flow is new, and this guide
recommends living there for your first
real library. The lab, being unattended
and working on throwaway fixtures,
turned on the server's **auto-accept**
setting (`autoAcceptTranscodes`) so its
runs could finish unwatched; the
verification notes in `criteria.md`
record that the manual accept path was
therefore not exercised. Your first
library should not be so lucky: stage,
inspect, accept by hand, and automate
only what you have watched succeed.

## Job reports

Every piece of work — each health
check, each transcode, success or
failure — writes a **job report**: a
step-by-step log of which node and
worker took it, which plugins ran, what
each one answered, the exact converter
command, and how it ended. The web
interface shows them; the server keeps
them as text files under its data
folder. They are long, repetitive, and
absolutely the first place to look when
anything surprises you. Chapter 6 reads
one properly, and the lab's transcripts
quote them throughout.
