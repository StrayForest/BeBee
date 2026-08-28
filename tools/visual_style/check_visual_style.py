#!/usr/bin/env python3
"""Validate the BB-P007 style contract and deterministic generated reference frames."""
from __future__ import annotations

import hashlib
import json
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from generate_reference_frames import CONFIG, generate


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_generated(paths: list[Path], approved: list[dict[str, object]]) -> None:
    require(len(paths) == len(approved) == 8, "expected eight generated BB-P007 reference frames")
    by_id = {item["id"]: item for item in approved}
    for path in paths:
        frame_id = path.stem
        require(frame_id in by_id, f"unexpected frame: {frame_id}")
        root = ET.parse(path).getroot()
        expected = by_id[frame_id]["viewport"]
        require(int(root.attrib["width"]) == expected[0], f"width mismatch: {path}")
        require(int(root.attrib["height"]) == expected[1], f"height mismatch: {path}")
        require(root.attrib.get("viewBox") == f"0 0 {expected[0]} {expected[1]}", f"viewBox mismatch: {path}")


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    require(cfg.get("schema_version") == 1, "schema_version must be 1")
    require(cfg.get("ticket") == "BB-P007", "ticket must be BB-P007")
    require("reference_viewport" in cfg, "reference viewport missing")
    viewport = cfg["reference_viewport"]
    require((viewport["width"], viewport["height"]) == (1280, 720), "reference viewport must remain 1280x720 unless V-001 changes")
    require(viewport["aspect_ratio"] == "16:9", "reference aspect ratio must be 16:9")
    require(viewport["primary_orientation"] == "landscape", "BB-P007 baseline orientation must be landscape")

    bee = cfg["world_scale"]["bee_screen_height_ratio"]
    require(0 < bee["min"] <= bee["nominal"] <= bee["max"] < 0.25, "invalid bee screen-height ratio")
    require(abs(cfg["world_scale"]["bee_reference_height_px"] / viewport["height"] - bee["nominal"]) < 0.002, "bee nominal ratio and reference pixels disagree")
    zoom = cfg["world_scale"]["camera_zoom_multiplier"]
    require(0.75 <= zoom["min"] <= zoom["default"] <= zoom["max"] <= 1.25, "invalid ordinary camera zoom band")
    require(cfg["camera"]["projection"] == "orthographic", "BB-P007 camera projection must be orthographic")
    require(cfg["rendering"]["texture_filtering"] in {"linear", "nearest"}, "unknown texture filter")
    require(cfg["ui"]["minimum_touch_hitbox_px_at_reference"] >= cfg["ui"]["button_visual_height_px"]["min"], "touch hitbox must not be smaller than visual button minimum")
    require(cfg["ui"]["persistent_hud_item_target"]["default_max"] <= 2, "default HUD target exceeds BB-P007 sparse-HUD baseline")
    require(cfg["ui"]["persistent_objective_count_max"] == 1, "default gameplay must expose at most one persistent objective")
    require(cfg["vfx"]["low_end_total_live_particles_max"] <= cfg["vfx"]["total_live_particles_target_max"], "low-end VFX budget exceeds baseline")

    approved = cfg["approved_frames"]
    frame_ids = [item["id"] for item in approved]
    require(len(frame_ids) == len(set(frame_ids)) == 8, "approved frame list must contain eight unique BB-P007 anchors")

    with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
        paths_a = generate(CONFIG, Path(first))
        paths_b = generate(CONFIG, Path(second))
        validate_generated(paths_a, approved)
        validate_generated(paths_b, approved)
        bytes_a = {p.name: p.read_bytes() for p in paths_a}
        bytes_b = {p.name: p.read_bytes() for p in paths_b}
        require(bytes_a == bytes_b, "reference-frame generation is not deterministic")
        expected_hashes = cfg["reference_frame_generation"]["sha256"]
        actual_hashes = {
            Path(name).stem: hashlib.sha256(payload).hexdigest()
            for name, payload in bytes_a.items()
        }
        require(actual_hashes == expected_hashes, "generated reference-frame hashes differ from the approved BB-P007 anchors")

    print("BB-P007 visual style contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
