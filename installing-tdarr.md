# Installing Tdarr

**Outcome: a Tdarr server running on
your machine, answering on its web port,
with its start-up self-tests read and
understood — before any library, flow or
node enters the picture.** The server and
node are separate downloads that live in
one folder; this chapter installs the
pair and starts the server alone.

## The two ways in

Tdarr is published from the project's own
storage, with a version index at
`https://storage.tdarr.io/versions.json`
naming every release and its per-platform
packages. (There are no GitHub release
downloads and no system packages; the
project ships its own.) The lab installed
**3.04.00**, the newest in the index at
the time, for 64-bit Linux (`linux_x64`;
ARM builds sit beside it).

The recommended route is the
**Tdarr_Updater**: a small bootstrapper
zip. Unzip it, run `Tdarr_Updater`, and
it fetches the server and node packages
of the current release and keeps them
current when re-run — the project's own
stand-alone updater, independent of the
update settings inside Tdarr itself.

The documented alternative — the one the
lab actually used, for reasons
transcript `t00` tells in full — is to
download the two packages directly and
unzip them side by side:

```bash
curl -sL -o Tdarr_Server.zip \
  https://storage.tdarr.io/versions/3.04.00/linux_x64/Tdarr_Server.zip
curl -sL -o Tdarr_Node.zip \
  https://storage.tdarr.io/versions/3.04.00/linux_x64/Tdarr_Node.zip
unzip Tdarr_Server.zip
unzip Tdarr_Node.zip
```

The zips are large (about 230 MB each)
because the programs carry their
runtimes with them. Both unpack into
*one* shared folder:

```text
Tdarr_Server, Tdarr_Node   the programs (plus tray variants)
rust/                      the engine binaries they launch
assets/app/ffmpeg/         bundled ffmpeg and ffprobe
assets/app/ccextractor/    bundled closed-caption tool
node_modules/, public/, runtime/, srcug/
```

Nothing is installed into the system: no
package manager, no administrator
rights, and deleting the folder removes
Tdarr completely. The lab's Updater
failure is worth one sentence here
because home networks cause it too: the
sandbox's web proxy would not carry the
Updater's requests, and the same failure
later blocked the server's built-in
plugin updater (chapter 13). On an
ordinary home connection neither has
anything to block it; the direct
packages are the fallback, not a
different product.

Two companions from the system's own
shelf matter: `mkvpropedit` (from the
mkvtoolnix package) is expected on the
path for tidying Matroska metadata, and
**HandBrakeCLI** is *not* bundled at
all — parts of Tdarr, including the
default health-check setting, assume you
have installed it yourself. Chapter 7
shows what happens when it is missing,
and how to choose the bundled ffmpeg
instead.

## The first start

```bash
./Tdarr_Server
```

It runs in the console, logging as it
goes (run it under your service manager
of choice later; nothing about Tdarr
needs systemd). First run creates, next
to the program folder: `configs/` (the
server's and later the node's settings
files), `server/Tdarr/` (the database,
plugins, logs and backups), and `logs/`.
Two ports open: **8265** for the web
interface and API, **8266** for nodes to
connect to.

Then it tests its own tools, and the lab
asks you to actually read this part,
because two of its lines look like
failures and one real failure hides
among them:

```text
Binary test 1: handbrakePath not working
Binary test 2: ffmpegPath not working
Binary test 3: mkvpropeditPath working
Scanner test 1: FFprobe working
Scanner test 2: Exiftool working
Scanner test 3: Mediainfo working
Scanner test 4: CCExtractor not working:
  …libtesseract.so.4: cannot open shared object file…
```

- *handbrakePath not working* — true, and
  expected until you install HandBrakeCLI
  or point the path at it. Not fatal;
  chapter 7 routes around it.
- *ffmpegPath not working* — the *custom
  path* is empty, which the test reports
  as not working; the bundled ffmpeg it
  falls back to demonstrably works
  (chapter 6's transcode runs it, and
  the scanner tests just below use its
  sibling ffprobe).
- *CCExtractor not working* — the bundled
  closed-caption extractor wants a system
  library (`libtesseract.so.4`) the lab
  did not have. It only matters if you
  ask Tdarr to detect closed captions;
  the lab did not, and ignored it, which
  the message itself blesses.

## The checks

The server is up when its status call
answers (transcript `t02`):

```bash
curl -s http://127.0.0.1:8265/api/v2/status
```

```json
{"status":"good","isProduction":true,"os":"linux","version":"3.04.00","buildDate":"2026_10_27T16_56_14z","uptime":36,"serverEngine":"rust"}
```

And the web interface itself answers at
`http://127.0.0.1:8265` in a browser —
replace the address with your server's
name or IP when working from another
machine.

## The sign-in, and a warning with teeth

A fresh server has **no users**, and its
first run in the web interface is a
setup wizard that creates an
administrator account. Until it exists,
most of the API refuses with
`{"status":401,"message":"No users","setupAdmin":true}`
— that refusal is the wizard's doorbell,
not an error. Create the account.

The server's settings file
(`configs/Tdarr_Server_Config.json`)
carries an `auth` switch, and the lab —
driving everything through the API on a
loopback-only sandbox, with no wizard —
turned it off to proceed. **Do not copy
that step on any machine whose ports
8265 or 8266 can be reached by anyone
you do not completely trust.** With auth
off, anyone who can reach the port can
run the whole of Tdarr, including flows
that rewrite and delete files. The lab's
circumstances (a disposable sandbox,
loopback only, both programs stopped at
the end) are the whole justification;
your media server's are unlikely to be.
Chapter 12 returns to this.

## The other doors

Tdarr is also published as Docker images
(server and node separately), which is
how many people run it; this guide's lab
used the native packages, by the series'
no-containers rule, and the Docker route
is documented-only here. Everything after
this chapter assumes the native layout
above, but nothing else differs: same
ports, same interface, same config
files, one folder deeper.
