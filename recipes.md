# Recipes

**Outcome: five variations on the
chapter 5 flow, each one change at a
time — and a clear line between the
ones the lab ran and the ones it only
designed.** The first recipe is the
lab's own flow restated as a starting
point; the rest reuse plugins from the
same community library. Where a recipe
rests on plugins the lab installed but
did not execute, the recipe says so.

## 1. Everything to H.264, audio untouched

The lab's flow, verbatim in structure:
**Input File → Check Video Codec
(`h264`) → output 2 → Begin Command →
Set Video Encoder (`h264`, preset
`veryfast`, quality `23`, hardware off)
→ Execute → Replace Original File**,
with output 1 unwired. Ran for real;
transcripts `t04`–`t06`. This is the
right first flow for almost everyone:
one rule, visibly enforced, nothing
else touched.

## 2. Audio to AAC as well

*Designed on lab-run pieces; the audio
half was not separately run.* Add a
second check after the first, or start
the chain with **Check Audio Codec**
(`checkAudioCodec`, input codec `aac`)
wired the same way: passing files fall
out, failing files enter the command
chain — and inside the chain, add **Set
Audio Encoder** beside Set Video
Encoder before Execute. Files failing
*both* checks now get both streams
rebuilt in one pass through the cache;
files failing neither keep falling out
untouched. The discipline is the
recipe: one check per rule, one
encoder per failing check, one Execute
for the whole command.

## 3. Cap the library at 1080p

*Designed, not run.* Insert **Check
Video Resolution** ahead of the encoder
chain, with its maximum height set to
1080, and give the chain a **Set Video
Resolution** step (maximum height 1080;
the encoder preserves the aspect ratio)
on the failing wire. Standard
definition and 720p files fall out the
passing wire; only the tall ones are
rebuilt, smaller in both senses. Pair
it with recipe 1's codec check in
series — a file can fail either,
neither, or both, and the chain handles
each case once.

## 4. Keep the original: convert to an output folder

Change one wire in recipe 1: replace
**Replace Original File** with **Move
To Directory**, whose single input is
the output folder, and set the library's
output folder to match. The source
library is now only ever read; results
collect elsewhere, and the catalogue
tracks the new files as the library's
own. This is the honest way to trial a
flow against a real library —
everything chapter 8's checks can see,
nothing they cannot undo — and the way
folder-to-folder conversion (ripping a
fresh batch into a finished library)
is meant to run.

## 5. Turn hardware encoding on — carefully

On a machine with a supported GPU:
in Set Video Encoder, set
`hardwareEncoding` and
`hardwareDecoding` on, `hardwareType`
to your card family rather than `auto`
once you know it works, and — this is
the recipe's actual instruction — run
it against **one small library first**,
then compare the job reports against a
CPU run of the same file: the command
line should name the hardware encoder,
the output should probe identically in
codec and duration, and the time should
be the point. The lab had no GPU and
ran this recipe exactly zero times;
its presence here is documentation,
labelled as such, because "the option
exists" and "the option helped" are
different claims and only one of them
is this guide's to make.

## 6. The classic plugin stack (the other decision maker)

The library template's default: an
ordered *list* of classic community
plugins — the lab's copy carried the
well-known Migz set (remove image
streams; reorder streams; transcode to
MKV keeping H.264/H.265) — run top to
bottom instead of through a wired flow.
If you arrive at Tdarr with an existing
stack from another user, it still works
and the interface still offers it as a
decision maker; new builds should start
with flows, which show their branching
instead of implying it. The lab
installed the 107-plugin classic
library alongside the flow plugins but
ran no classic stack end to end — the
default stack's presence in the
template is documented here, its
behaviour is the community's to
describe.
