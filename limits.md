# Limits

**Outcome: the edges of the tool, stated
before they cost you a file — including
the two limits that are really about
trust: destructive replacement, and
security that is your job, not Tdarr's.**

## Replacement is destructive, by design

A flow ending in Replace Original File
deletes the original. The swap itself is
careful (chapter 6: verified sizes,
renames, no window left without a file),
but careful is not reversible: there is
no undo, no recycle bin, no "previous
version" in Tdarr. A flow that converts
at the wrong quality, crops wrongly, or
drops a stream you wanted has not made
an error you can roll back — it has made
a *smaller library*, correctly, quickly,
and at scale. Your backups are the undo.
Stage first (chapter 2), convert small
libraries first (chapter 10), and never
let a new flow meet an un-backed-up
library.

## A flow is only as good as its plugins

Tdarr's judgement is borrowed: checks
read the catalogue, and the catalogue is
only what the probers reported. A file
whose metadata lies — a stream
mislabelled, a container pretending —
will be judged by the lie. Plugins are
community code of community quality:
the popular ones are battle-tested, the
long tail is one person's script, and a
flow chains them sight unseen unless
you read the job reports (chapter 6
exists so you can). Plugin *updates*
arrive from the project's repository on
the server's schedule, not yours; a
library that runs untouched for a year
is running year-old judgement. And the
chapter 5 trap is the standing example:
the flagship encoder plugin *defaults*
to a different codec than the one this
guide wanted. Defaults are decisions
somebody else made.

## One decision maker per library

A library is judged by exactly one
thing — a flow, a classic stack, or the
basic settings — and one flow has one
chain of wires per file. There is no
"also run this other flow and combine
the verdicts", no per-subfolder policy
inside a library (that is what more
libraries are for), and no dry-run mode
that reports what a flow *would* do
without doing it; the honest trial is
chapter 10's output-folder recipe, run
on copies. Go To Flow chains soften the
first of these for advanced users; the
shape of the limit remains.

## It converts files. That is all

No playback, no posters, no library
browsing, no awareness of what a film
*is* — a file misfiled in the wrong
library will be converted to that
library's standard with perfect
obedience. No downloading, renaming or
organising. No repair: a file that
fails its health check is reported, not
healed, and Tdarr will not rescue the
watchable half of a damaged recording.
No scheduling brain beyond worker
counts by the hour: "convert the new
arrivals before the weekend, cheaply,
while the house is empty" is three
settings in three places, not one
intention.

## The security line, plainly

Tdarr is a remote-control system for
file-rewriting machinery, and its
defaults fit a trusted home network and
no other place:

- The server asks for a login **if you
  create one in the first-run wizard**;
  the lab's transcript shows the
  `auth: false` alternative existing —
  and chapter 3 says why it must stay a
  lab-only move. With auth off, port
  8265 is an open door to flows that
  delete files.
- Nodes join by address, without a
  pairing secret worth the name. Port
  8266 reachable by strangers means
  strangers volunteering to run your
  plugins.
- Plugins are other people's code,
  executed by your node with your file
  permissions, fetched from a repository
  over the network. The popular set is
  widely used and reviewed in public;
  "widely used" is the assurance on
  offer, and it is not a sandbox.

Run it the way it asks to be run —
auth on, ports on your own network
only — and those are footnotes. Run it
any other way and they are the review.

## The price of free

The core of Tdarr — server, nodes,
flows, the community plugin library —
is free to use, and everything this
guide ran was the free core. The
project also sells a **Pro** tier that
unlocks extras around the edges
(advanced statistics, notifications and
similar comforts). Nothing in the lab's
work needed it, no chapter here depends
on it, and the guide takes no position
on its value beyond noting the line
exists: if a screen in your interface
asks for a licence, you have wandered
into the extras, not out of the tool.
