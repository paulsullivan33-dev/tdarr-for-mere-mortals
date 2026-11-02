# Nodes and Workers

**Outcome: the model for growing past
one machine — what a node needs to
join, how its workers and schedule
shape its manners, and where the
boundaries of the lab's evidence lie.**
Everything in this guide so far happened
on one machine wearing two hats. This
chapter separates the hats.

## A node joins by address, not by discovery

A node is configured, not discovered.
Its settings file
(`configs/Tdarr_Node_Config.json`, in
the same shared folder layout as the
server's) carries the essentials:

```json
{
  "nodeName": "good-gar",
  "serverIP": "127.0.0.1",
  "serverPort": "8266",
  "serverURL": "http://127.0.0.1:8266"
}
```

Point those at the machine running your
server — a real network address this
time, not loopback — start the node,
and it registers: the server notes its
name, its network address, and its
worker limits, and begins offering it
jobs from every library's queue. There
is no pairing ceremony and no shared
secret in the default setup, which cuts
both ways: joining is effortless, and
anything that can reach port 8266 can
offer to work — one more reason chapter
3 insists the server's ports belong on
networks you trust.

The lab's one real node lesson belongs
here, because it generalises: the
node's *default* address for its own
server was `0.0.0.0`, which means "this
machine" only by courtesy, and on the
sandbox that courtesy failed (the
handshake went to a proxy; transcript
`t02`). Put the actual address — a
number or a name that resolves — in the
node config, on every node, even the
one that shares the server's machine.
Node and server also keep each other
honest about the plugins: the server
bundles its plugin library for nodes to
load from, so a node never needs its
own copy of your flows' plugins.

## Workers are the capacity, schedules are the manners

Chapter 6 set the lab's node to one
transcode worker and one health-check
worker. The general rule behind that
choice: a CPU transcode worker will
happily eat every core you let it see,
so **workers × appetite = the machine's
opinion of Tdarr**. One worker on a
shared machine is a polite guest; four
on a dedicated box is the point of the
box. GPU workers, where the hardware
and drivers exist, take the encoding
onto the graphics card — the flow asks
the same questions, the worker pool
that answers is different (the lab had
no GPU; the pools exist in the
interface, and chapter 5 explains why
the flows left hardware encoding off).

Each node also carries an hourly
**schedule** of worker limits — the
grid the server kept in its records
runs 00–01 through 23–00 per day. Its
natural uses: full strength overnight,
zero workers during the hours the
machine is a workstation, health checks
only on Sunday afternoons. A node that
is *paused* (or started with
`startPaused`) registers but takes
nothing until released — the right
state for a laptop node you carry away
mid-queue; jobs it was running are
requeued by the server, not lost with
it.

## Mapped and unmapped, paths and translators

The lab's node was a **mapped** node: it
and the server agreed on file paths,
because they shared a disk. A node on
another machine usually shares the
library over the network, and then the
question is what the *same folder* is
called on each side. **Path translators**
— pairs in the node config, server path
on the left, node path on the right —
rewrite the library and cache paths as
jobs cross over: the classic case is a
Windows node serving a Linux server,
drive letters on one side, slashes on
the other. Get them wrong and the node
reports, accurately, that the file in
the job does not exist.

**Unmapped** nodes (a newer kind) skip
the shared folder entirely: the server
sends the node the file itself, the
node works on its own cache, and sends
the result back. It costs a full copy
of every file across the network in
each direction, and buys nodes that
need no shares, no mounts and no path
agreement at all — a laptop joining for
the evening, say. The lab did not run
one (its single node shared a disk by
construction), so unmapped nodes are
described from the documentation here,
and flagged as such in `criteria.md`.

## The honest boundary

The lab proved: registration, worker
limits, and job execution for one node
on the server's own machine, over
loopback. It did not prove: a node on a
second machine, a GPU worker, a
schedule change taking effect, path
translators, or unmapped nodes. Those
are written from the project's
documentation and the settings the
server itself recorded, and the text
has not claimed otherwise. The shape of
the whole chapter, though, is the shape
of the system: *capacity is workers,
manners are schedules, and reach is one
config file.* Adding your second
machine is an afternoon, not a rebuild.
