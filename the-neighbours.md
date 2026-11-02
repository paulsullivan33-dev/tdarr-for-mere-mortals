# The Neighbours

**Outcome: an honest map of the tools
that share Tdarr's fence line — what
each does better, what Tdarr does that
they do not, and when to reach for
which.** The neighbours are
characterised here, not benchmarked;
the two in this series with guides of
their own are pointed to, once each,
by name.

## HandBrake: the converter itself

HandBrake (and its command-line form,
HandBrakeCLI) converts video superbly:
presets that make sense, hardware
encoding, a queue you build by hand.
What it does not do is *patrol*. A
HandBrake queue is a list you made;
when it finishes, it forgets. Tdarr is
weaker as a converter — much of its
transcoding is literally HandBrake's or
ffmpeg's work, directed by plugins —
and stronger as a system: the standing
rule, the catalogue, the queue, the
second machine. If you have twelve
files to convert once, HandBrake is the
shorter path, and this series' guide to
it is the one to read. If you have a
library that keeps *arriving*, that is
the gap Tdarr fills — and chapter 7
shows the two cooperating, Tdarr
calling HandBrake for its health checks
when it is installed.

## ffmpeg, driven by hand (or by script)

Everything Tdarr's flow plugins build
ends as an ffmpeg command — chapter 5
printed one in full. A folder of your
own scripts over ffmpeg (this series
has a guide) gives you total control
and total responsibility: no catalogue
unless you keep one, no queue unless
you build one, no "not required" verdict
unless you write the check. For a
handful of files or a transformation
too odd for the plugin library, the
direct tool wins on honesty alone. For
a library, the script folder quietly
becomes a worse Tdarr, one feature at a
time. The boundary the lab suggests:
script it while the rule fits in one
command you can hold in your head;
flow it when the rule has branches,
exceptions, or a schedule.

## FileFlows and Unmanic: the same job, other workshops

Two community tools work the same beat.
**FileFlows** generalises the flow idea
beyond video — files of any kind move
through node chains (its heritage is
the same plugin thinking) — and suits
people whose "library" is documents,
images and downloads as much as films.
**Unmanic** keeps a tighter scope than
Tdarr (a plugin-driven library
optimizer with a simpler, single-machine
centre of gravity) and suits people who
found Tdarr's server/node split more
machinery than their setup needs.
Neither is a failed Tdarr; both are the
same insight — *state a standard, let
the machine enforce it* — at different
weights. The honest selection test is
the shape of your problem: one machine
and video only (Unmanic's weight), any
file and flow-shaped problems
(FileFlows'), or video with spare
machines and a big catalogue (Tdarr's).

## The media server is not a neighbour but a partner

Jellyfin, Plex and their kin appear in
Tdarr conversations as if they were
rivals. They are the other half of the
story: servers play, Tdarr prepares.
The complete home setup this series
describes across its guides is a
library the media server streams, kept
to a standard by flows, on hardware
whose spare hours the nodes borrow.
Choosing between them is a category
error; choosing the order to install
them is not — get playback working
first, because a library nobody can
watch is not improved by being tidier.
