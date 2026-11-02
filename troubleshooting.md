# Troubleshooting

**Outcome: the failures this guide's lab
actually had — every one of them — each
with the evidence that named it and the
fix that closed it, plus the order to
check things in when yours differs.**
Every item below is drawn from the
lab's transcripts; nothing here is
invented for completeness.

## The order to check things

1. The **job report** for the failed
   job. It names the step and keeps the
   error in the step's own words. Most
   entries below end with "the report
   said so".
2. The **server and node logs** — the
   server's start-up tests and the
   node's connection attempts are
   written there in plain language.
3. The **worker's existence** — node
   registered? Worker counts above zero?
4. Only then: the file itself.

## The node never appears (or appears and does nothing)

*Evidence:* `get-nodes` shows `{}` long
after the node started; the node's log
repeats a failed "version-check" POST.
*Cause, in the lab:* the node config's
default server address, `0.0.0.0`, sent
its handshake somewhere that was not
the server (on the sandbox, an HTTP
proxy — the log's line `CONNECT proxy
failed` confessed it). *Fix:* write the
server's real address into
`Tdarr_Node_Config.json` — `serverIP`
and `serverURL` — a number or a name
that resolves, even on the same machine
(use `127.0.0.1`, not `0.0.0.0`).
Transcript `t02`.

*Second cause, same symptom:* the node
appears, green and registered, and no
job ever moves. Check its worker
limits: a brand-new node's are all
**zero**. Raise at least one transcode
and one health-check worker (chapter
6). This is the most common state in
Tdarr to be mistaken for a fault.

## Every flow job fails at the first plugin

*Evidence:* job report, first or second
plugin step: `Error: Cannot find module
'../../../../FlowHelpers/1.0.0/fileUtils'`.
*Cause:* the community plugin library
was installed one folder short — the
flow plugins expect their shared
**FlowHelpers** folder beside them, and
a partial copy (plugins without
helpers) loads far enough to fail
exactly like this. *Fix:* install the
*whole* plugin library — flow plugins,
templates, **FlowHelpers**, classic
plugins — then restart the server (so
it re-bundles the library for nodes)
and the node. Transcript `t04`,
attempt 1.

## Every flow job fails one step later, in Input File

*Evidence:* `Error: Cannot find module
'../../../../../methods/lib'`, with
Input File at the top of the require
stack. *Cause:* the same partial
install, one folder deeper — the
plugins also require the repository's
**methods** folder at the plugin
library's root. *Fix:* as above; the
two failures are one lesson wearing
two coats: *plugin installs are
all-or-nothing.* Transcript `t04`,
attempt 2.

## Health checks all fail in seconds

*Evidence:* health check report:
`Error executing binary: HandBrakeCLI —
No such file or directory`, jobs dying
in under four seconds. *Cause:* the
library's health checks are set to
HandBrake (the template default) and
HandBrakeCLI is not installed — it is
not part of Tdarr's download. *Fix:*
install HandBrakeCLI, or switch the
library's health-check tool to ffmpeg
(chapter 7). Nothing is wrong with any
file; an Error verdict from a missing
*tool* is indistinguishable from a
broken file until the report's last
lines — which is why those reports are
checked first. Transcript `t04`.

## The plugin library will not update

*Evidence:* server log at start-up:
`Error checking latest plugin repo
commit: io: invalid peer certificate:
UnknownIssuer`, then `[Plugin Update]
Could not resolve a target SHA;
aborting`. *Cause:* something between
the server and the project's repository
is interfering with the connection —
in the lab, the sandbox's proxy and
its certificate; on a home network, an
over-eager security appliance or a
genuine outage. Tdarr keeps running on
the plugins it has. *Fix:* fetch the
plugin repository as a zip from the
project's GitHub with a tool that can
get through, and lay its contents
under the server's `server/Tdarr/Plugins/`
folder — complete, per the two entries
above. Check your network path first if
you did not expect a proxy at all.

## The Updater will not update

*Evidence:* `Tdarr_Updater — Failed to
get package index after retries`, while
a browser or curl reaches the project's
storage fine. *Cause:* the same network
interference, one level up. *Fix:* the
project documents direct Server and
Node packages per release in its
version index (`storage.tdarr.io/versions.json`);
download the pair for your platform,
stop Tdarr, unzip them over the
existing folder, restart. The lab
installed this way from the start
(transcript `t00`) and nothing about
the result differs.

## Closed captions never detected

*Evidence:* start-up log, `Scanner test
4: CCExtractor not working …
libtesseract.so.4: cannot open shared
object`. *Cause:* the bundled
CCExtractor wants a system library the
machine lacks. *Fix, if you need
caption detection:* install the
tesseract library the message names
(its own text gives the apt line).
*Fix, if you don't:* none — the warning
is honest about its own irrelevance,
and every other scanner test passing
is the install working as intended.

## A transcode "succeeds" but nothing changed

*Evidence:* job verdict *Not required*;
the report shows a check plugin taking
its **passing** output (`outputNumber:
1`) and the flow ending. *Cause:* the
file already met the standard — the
system working, chapter 8's third row.
If you expected conversion anyway, the
usual suspects, in order: the check's
input names a different codec than you
think (read it in the report, where the
loaded inputs are printed); the encoder
plugin's `outputCodec` default
(`hevc`) means the flow *writes* a
different codec than the check *tests
for* — a library can convert its own
output forever that way; or the file
you are looking at is not the file in
the library (two copies, one folder
apart, is the classic).
