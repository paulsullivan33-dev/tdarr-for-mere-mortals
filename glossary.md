# Glossary

**Auto-accept** — the server setting
(`autoAcceptTranscodes`) that lets a
finished transcode replace its original
without waiting for a human in the
staging area. Off by default; the lab
turned it on, on throwaway fixtures.

**Begin Command / Execute** — the flow
plugins that open and run an ffmpeg
command. Between them sit the plugins
that set what the command does.

**Cache (transcode cache)** — the
folder where a node builds a converted
file before it is swapped into place.
Per library; needs room for a second
copy of your largest file.

**Catalogue** — the server's record of
every scanned file: streams, codecs,
sizes, and verdicts. Flows judge the
catalogue, not the disk.

**Classic plugin stack** — the older
decision maker: an ordered list of
classic plugins run top to bottom,
instead of a wired flow.

**Decision maker** — the library
setting that chooses what judges its
files: a flow, the classic stack, or
the basic video/audio settings. One
per library.

**Flow** — a chain of plugins wired
output to input, expressing one
standard. Starts with Input File;
ends wherever the wires run out.

**FlowHelpers** — the shared library
the community flow plugins stand on.
A plugin install missing it fails at
the first plugin (chapter 13).

**HandBrakeCLI** — HandBrake's
command-line form. Not bundled with
Tdarr; the default health-check tool
and one of its two transcoding
engines. The other is ffmpeg.

**Health check** — a job that probes a
file for damage by reading or decoding
it. Quick checks sample; thorough
checks decode end to end. Verdicts:
Success or Error.

**Job report** — the step-by-step text
record of one job: server, node,
worker, plugins, command, verdict.
The first place to look, always.

**Library** — a folder plus its
settings: cache, scan options, and a
decision maker. The unit of policy.

**Mapped / unmapped node** — a mapped
node shares the library's paths with
the server (possibly through path
translators); an unmapped node is sent
the files themselves and returns the
results.

**Node** — the worker program that
connects to the server (port 8266),
asks for jobs, and runs them. Named
at random until you rename it.

**Not required** — the transcode
verdict for a file that passed its
flow's checks and was left untouched.
A success state, and the common one.

**Path translator** — a pair of paths
in a node config (the server's name
for a folder, the node's name for the
same folder) rewritten as jobs cross
between machines.

**Plugin** — one check or action in a
flow or classic stack. Community
plugins are shared by users; local
ones are your own.

**Scan (Find new) / Scan (Fresh)** —
the two catalogue scans: add what is
new or changed, or discard the
catalogue and probe everything again.

**Server** — the always-on program:
catalogue, libraries, flows, queue,
web interface (port 8265). The brain;
nodes are the muscle.

**Staging area** — where finished
transcodes wait for acceptance before
replacing originals, when auto-accept
is off.

**Tdarr_Updater** — the stand-alone
bootstrapper that downloads and
updates the server and node packages.
Independent of the update settings
inside Tdarr.

**Worker** — a node's unit of
capacity: transcode or health check,
CPU or GPU. New nodes have zero of
each until you grant some.
