# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's fixtures are generated test patterns with
   invented titles.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 12 names what the tool
   cannot do: replacement of originals is destructive and
   irreversible, a flow's judgement is only as good as its
   community plugins and the probe data they read, one library
   gets exactly one decision maker, there is no dry-run, no
   playback or organising, no repair of damaged files — and
   the built-in conveniences (auto-accept, plugin updates)
   trade safety for quiet in ways the chapter spells out.
8. **The ethics and safety rule is in the text, early.**
   Tdarr rewrites and deletes media files on your say-so, so
   chapter 1 states the standing order plainly — a careless
   flow damages your own library at scale — and chapters 3
   and 12 draw the security line before any procedure depends
   on it: leave sign-in on, keep ports 8265 and 8266 on
   networks you trust, and remember that community plugins
   are other people's code running with your permissions.
   The lab itself ran fixtures it generated, on loopback,
   with sign-in disabled only inside a disposable sandbox,
   and says so wherever the step appears.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a shared Ubuntu 24.04 sandbox with no
containers and no GPU. Tdarr **3.04.00** (server and node,
linux_x64) was installed from the project's own storage
(`storage.tdarr.io`, per its `versions.json` index). The
Tdarr_Updater was tried first and genuinely attempted: its
requests could not cross the sandbox's web proxy, so the
project's documented direct packages of the same version were
used instead (transcript t00). The server and node ran on
Tdarr's own default ports (web/API 8265, node port 8266) on
loopback, as the assignment for this guide allowed, and both
were shut down when the lab finished. The server's built-in
plugin updater failed the same way (TLS "UnknownIssuer"
through the proxy), so the community plugin library was
fetched as a zip of the project's own repository
(HaveAGitGat/Tdarr_Plugins, master as of the lab date) and
laid under the server's Plugins folder complete — after two
recorded failures (t04) taught the lab that a partial plugin
install is worse than none. All transcripts live in
`tdarr-lab/transcripts/`; the fixture generator is
`tdarr-lab/make-fixtures.sh`, the flow and library documents
are `tdarr-lab/lab-flow.json` and `tdarr-lab/library.json`,
and the API driver is `tdarr-lab/make-flow-library.py`.

Sign-in: a fresh server has no users. The lab drove Tdarr
through its API on a loopback-only sandbox and set the
server config's own `auth` switch to false to proceed. That
step is labelled a lab-only move in chapters 3 and 12; the
first-run wizard and normal authenticated use were therefore
not exercised, and are described from the documentation.

Run for real, with transcripts as evidence:

- Version index read, Updater attempted and failed on the
  proxy, direct Server/Node packages (3.04.00) downloaded and
  unpacked; the bundled ffmpeg identified as 7.1.4-Jellyfin
  and run directly (t00).
- Fixtures generated with the system ffmpeg 8.1.2 and probed
  before any Tdarr contact: MKV (mpeg2video + mp2, 1,736,532
  bytes), AVI (mpeg4 + mp3, 721,048 bytes), and later an MP4
  (h264 + aac, 483,259 bytes) (t01).
- Server first start: config and data folders created,
  start-up binary/scanner tests read (HandBrakeCLI absent,
  mkvpropedit present, CCExtractor missing libtesseract.so.4),
  `/api/v2/status` answering version 3.04.00; the 401 "No
  users" state observed before auth was switched off (t02).
- Node first start: random name assigned, connection failure
  against the default `0.0.0.0` server address diagnosed from
  its log (proxy), fixed by addressing 127.0.0.1; node
  registered; worker limits raised from the default zero to
  1 transcode CPU and 1 health-check CPU (t02).
- A flow ("Lab Flow - Make H.264") and a library created
  through the server's own CRUD API — the library built from
  the web interface's default template with the changed
  fields listed — and read back as proof (t03).
- Library scans (Find new) and the full job cycle, including
  two failed attempts kept in the record: missing FlowHelpers
  folder, then missing methods folder, then health checks
  failing on the absent HandBrakeCLI until the library was
  switched to ffmpeg health checks (t04).
- End-to-end transcodes of both offending fixtures: the flow's
  own ffmpeg command (bundled ffmpeg, libx264, CRF 23,
  veryfast, audio copied), cache build, verified swap
  choreography, and after-probes: MKV 1,736,532 → 863,370
  bytes, AVI 721,048 → 292,666 bytes, video now h264, audio
  codecs unchanged; post-transcode health checks passing
  (t04, t06).
- Second Find new scan producing no new jobs, and the
  already-compliant MP4 passing the flow with the verdict
  "Not required" — check plugin output 1, no ffmpeg run, file
  untouched (t05).

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- The web interface itself (the lab used the API the
  interface calls) and the first-run admin wizard.
- Manual staging acceptance (the lab set auto-accept on, for
  unattended fixture runs) and folder watching.
- HandBrakeCLI-based health checks and HandBrake transcoding:
  the program is not bundled and was not installed; only the
  ffmpeg paths were exercised.
- GPU/hardware encoding (no GPU in the sandbox; the lab's
  flow disabled it on purpose), nodes on other machines,
  path translators, schedules taking effect, and unmapped
  nodes.
- The classic plugin stack as a decision maker (installed —
  107 classic plugins — but not run end to end), classic
  stack import into flows, Go To Flow chains, Docker
  installation, the Pro tier, and the neighbour tools of
  chapter 11.
- Recipes 2–6: built from plugins the lab installed and, for
  recipe 1's pieces, ran — but only recipe 1 was executed
  as written, and each recipe says which it is.
- Closed-caption detection (bundled CCExtractor lacks its
  system library here) and mkvpropedit metadata runs.

Fixtures are this guide's own and deliberately generic:
ffmpeg test patterns and sine tones under invented titles —
no real media, no real names, no one's library. The only
files Tdarr ever replaced in the lab were those fixtures,
inside the lab's own folders.
