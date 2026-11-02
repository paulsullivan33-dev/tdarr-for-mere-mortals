#!/usr/bin/env python3
"""Lab driver: create the Tdarr flow and library through the server's own
CRUD API (the same calls the web UI makes). Prints everything it sends
and receives so the transcript is the evidence."""
import json
import urllib.request

BASE = "http://127.0.0.1:8265/api/v2"


def cruddb(collection, mode, doc_id=None, obj=None):
    data = {"collection": collection, "mode": mode}
    if doc_id is not None:
        data["docID"] = doc_id
    if obj is not None:
        data["obj"] = obj
    body = json.dumps({"data": data}).encode()
    req = urllib.request.Request(
        BASE + "/cruddb", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode() or "null")


flow = {
    "_id": "labflowh264",
    "name": "Lab Flow - Make H.264",
    "description": "Files whose video is not H.264 are re-encoded to "
                   "H.264 with ffmpeg (other streams copied). H.264 "
                   "files pass through untouched. The result replaces "
                   "the original file.",
    "tags": "",
    "flowPlugins": [
        {"name": "Input File", "sourceRepo": "Community",
         "pluginName": "inputFile", "version": "1.0.0",
         "id": "inA", "position": {"x": 300, "y": 40}},
        {"name": "Check Video Codec", "sourceRepo": "Community",
         "pluginName": "checkVideoCodec", "version": "1.0.0",
         "id": "chkB", "position": {"x": 300, "y": 160},
         "inputsDB": {"codec": "h264"}},
        {"name": "Begin Command", "sourceRepo": "Community",
         "pluginName": "ffmpegCommandStart", "version": "1.0.0",
         "id": "cmdC", "position": {"x": 300, "y": 280}},
        {"name": "Set Video Encoder", "sourceRepo": "Community",
         "pluginName": "ffmpegCommandSetVideoEncoder", "version": "1.0.0",
         "id": "encD", "position": {"x": 300, "y": 400},
         "inputsDB": {"outputCodec": "h264",
                      "hardwareEncoding": False,
                      "hardwareDecoding": False,
                      "ffmpegPreset": "veryfast",
                      "ffmpegQuality": "23"}},
        {"name": "Execute", "sourceRepo": "Community",
         "pluginName": "ffmpegCommandExecute", "version": "1.0.0",
         "id": "exeE", "position": {"x": 300, "y": 520}},
        {"name": "Replace Original File", "sourceRepo": "Community",
         "pluginName": "replaceOriginalFile", "version": "1.0.0",
         "id": "repF", "position": {"x": 300, "y": 640}},
    ],
    "flowEdges": [
        {"source": "inA", "sourceHandle": "1", "target": "chkB",
         "targetHandle": None, "id": "e1"},
        {"source": "chkB", "sourceHandle": "2", "target": "cmdC",
         "targetHandle": None, "id": "e2"},
        {"source": "cmdC", "sourceHandle": "1", "target": "encD",
         "targetHandle": None, "id": "e3"},
        {"source": "encD", "sourceHandle": "1", "target": "exeE",
         "targetHandle": None, "id": "e4"},
        {"source": "exeE", "sourceHandle": "1", "target": "repF",
         "targetHandle": None, "id": "e5"},
    ],
}

print("INSERT flow into FlowsJSONDB:")
print(json.dumps(flow, indent=1))
print("RESPONSE:", cruddb("FlowsJSONDB", "insert", flow["_id"], flow))

print()
print("UPDATE global settings: autoAcceptTranscodes -> true")
print("RESPONSE:", cruddb("SettingsGlobalJSONDB", "update",
                           "globalsettings",
                           {"autoAcceptTranscodes": True}))

lib = json.loads(open("library.json").read())
print()
print("INSERT library into LibrarySettingsJSONDB:")
print(json.dumps(lib, indent=1)[:1200], "...")
print("RESPONSE:", cruddb("LibrarySettingsJSONDB", "insert",
                          lib["_id"], lib))

print()
print("Flows now:", json.dumps(cruddb("FlowsJSONDB", "getAll"))[:300])
print("Libraries now:",
      json.dumps(cruddb("LibrarySettingsJSONDB", "getAll"))[:300])
