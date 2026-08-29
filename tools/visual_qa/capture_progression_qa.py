#!/usr/bin/env python3
"""P3 browser proof for Hive purchases, felt effects, Buzz gate and reload."""
from __future__ import annotations
import hashlib, math, tempfile
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from playwright.sync_api import Browser, Page


def _url(base: str, **values: object) -> str:
    p=urlsplit(base); q=dict(parse_qsl(p.query, keep_blank_values=True)); q.update({k:str(v) for k,v in values.items()})
    return urlunsplit((p.scheme,p.netloc,p.path,urlencode(q),p.fragment))

def _sha(path: Path) -> str:
    h=hashlib.sha256();
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def _errors(page: Page):
    console=[]; page_errors=[]
    page.on('console', lambda m: console.append(m.text) if m.type in {'error','assert'} else None)
    page.on('pageerror', lambda e: page_errors.append(str(e)))
    return console,page_errors

def _assert_clean(console,page_errors,label):
    if console or page_errors: raise RuntimeError(f"{label}: console={console!r} page={page_errors!r}")

def _progress(page: Page) -> dict:
    v=page.evaluate("() => window.__bebeeProgressionQA ? structuredClone(window.__bebeeProgressionQA) : null")
    if not isinstance(v,dict): raise RuntimeError('progression bridge missing')
    return v

def _move(page: Page) -> dict:
    v=page.evaluate("() => window.__bebeeMovementQA ? structuredClone(window.__bebeeMovementQA) : null")
    if not isinstance(v,dict): raise RuntimeError('movement bridge missing')
    return v

def _wait(page: Page, head_sha: str, state: str, timeout_ms: int) -> dict:
    page.wait_for_function("() => window.__bebeeQA && window.__bebeeQA.captureReady === true && !!window.__bebeeProgressionQA && !!window.__bebeeMovementQA", timeout=timeout_ms)
    qa=page.evaluate("() => structuredClone(window.__bebeeQA)")
    if qa.get('stateId') != state or qa.get('buildCommitSha') != head_sha: raise RuntimeError(f'P3 provenance mismatch: {qa!r}')
    return _progress(page)

def _shot(page: Page, path: Path):
    path.parent.mkdir(parents=True,exist_ok=True); page.screenshot(path=str(path),full_page=False,animations='disabled')

def _record_hive_desktop(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict:
    frames=output_root/'p3_progression'/'desktop_reference_frames'; video_path=output_root/'p3_progression'/'desktop_reference.webm'; video_path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='bebee-p3-desktop-') as video_dir:
        context=browser.new_context(viewport={'width':1280,'height':720},screen={'width':1280,'height':720},device_scale_factor=1,record_video_dir=video_dir,record_video_size={'width':1280,'height':720})
        page=context.new_page(); video=page.video; console,page_errors=_errors(page)
        try:
            page.goto(_url(base_url,qa='progression_hive',qa_seed=88008,p3_storage_lifecycle='reset'),wait_until='load',timeout=timeout_ms)
            before=_wait(page,head_sha,'progression_hive',timeout_ms); _shot(page,frames/'00-hive-ready.png')
            if before.get('honey') != 45 or before.get('flightLevel') != 1 or before.get('buzzLevel') != 1 or before.get('hiveNearby') is not True:
                raise RuntimeError(f'P3 Hive fixture invalid: {before!r}')
            if before.get('flightNextCost') != 30 or before.get('buzzNextCost') != 35:
                raise RuntimeError(f'P3 prices not visible in bridge: {before!r}')

            page.keyboard.press('Space')
            page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === true",timeout=timeout_ms)
            opened=_progress(page); _shot(page,frames/'01-hive-panel.png')
            start=_move(page); page.keyboard.down('d'); page.wait_for_timeout(500); page.keyboard.up('d'); page.wait_for_timeout(150); blocked=_move(page)
            modal_displacement=math.hypot(float(blocked['beeX'])-float(start['beeX']),float(blocked['beeY'])-float(start['beeY']))
            if modal_displacement > 1.0: raise RuntimeError(f'movement leaked through Hive modal: {modal_displacement}')
            page.keyboard.press('ArrowLeft')
            page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.selectedUpgrade === 'flight'",timeout=timeout_ms)

            page.keyboard.press('Space')
            page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.flightLevel === 2",timeout=timeout_ms)
            bought=_progress(page); _shot(page,frames/'02-flight-purchased.png')
            if bought.get('honey') != 15 or bought.get('flightMaxSpeed') != 330: raise RuntimeError(f'Flight purchase effect mismatch: {bought!r}')
            page.keyboard.press('Escape'); page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === false",timeout=timeout_ms)
            page.keyboard.down('d'); page.wait_for_timeout(900); cruise=_move(page); page.keyboard.up('d'); page.wait_for_timeout(250)
            if float(cruise.get('maxSpeed',0)) != 330 or float(cruise.get('speed',0)) < 315: raise RuntimeError(f'Flight not felt in movement runtime: {cruise!r}')
            _shot(page,frames/'03-flight-cruise.png')

            page.wait_for_timeout(1200)
            page.goto(_url(base_url,qa='progression_hive',qa_seed=88008,p3_storage_lifecycle='reload'),wait_until='load',timeout=timeout_ms)
            reloaded=_wait(page,head_sha,'progression_hive',timeout_ms); _shot(page,frames/'04-reloaded.png')
            if reloaded.get('flightLevel') != 2 or reloaded.get('honey') != 15 or reloaded.get('flightMaxSpeed') != 330:
                raise RuntimeError(f'P3 Flight reload mismatch: {reloaded!r}')
            _assert_clean(console,page_errors,'P3 desktop Hive')
            result={'viewport':{'id':'desktop_reference','width':1280,'height':720},'before':before,'opened':opened,'modal_movement_displacement':round(modal_displacement,4),'bought':bought,'cruise':cruise,'reloaded':reloaded,'console_error_count':len(console),'page_error_count':len(page_errors)}
        finally: context.close()
        if video is None: raise RuntimeError('P3 desktop video handle missing')
        video.save_as(str(video_path))
    if not video_path.is_file() or video_path.stat().st_size == 0: raise RuntimeError('P3 desktop video missing')
    result['video_file']=video_path.relative_to(output_root).as_posix(); result['video_sha256']=_sha(video_path); result['frame_files']=[p.relative_to(output_root).as_posix() for p in sorted(frames.glob('*.png'))]
    return result

def _record_buzz_gate(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict:
    frames=output_root/'p3_progression'/'buzz_gate_frames'; context=browser.new_context(viewport={'width':1280,'height':720},screen={'width':1280,'height':720},device_scale_factor=1)
    page=context.new_page(); console,page_errors=_errors(page)
    try:
        page.goto(_url(base_url,qa='progression_buzz_gate',qa_seed=88008,p3_storage_lifecycle='reset'),wait_until='load',timeout=timeout_ms)
        locked=_wait(page,head_sha,'progression_buzz_gate',timeout_ms); _shot(page,frames/'00-buzz-locked.png')
        p3=locked.get('patch3') or {}
        if p3.get('state') != 'LOCKED' or p3.get('eligibilityReason') != 'requires_buzz' or p3.get('requirement') != 2:
            raise RuntimeError(f'Buzz gate not explicit before purchase: {locked!r}')
        page.keyboard.press('Space'); page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === true",timeout=timeout_ms)
        page.keyboard.press('ArrowRight'); page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.selectedUpgrade === 'buzz'",timeout=timeout_ms)
        _shot(page,frames/'01-buzz-selected.png')
        page.keyboard.press('Space'); page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.buzzLevel === 2",timeout=timeout_ms)
        unlocked=_progress(page); _shot(page,frames/'02-buzz-purchased.png')
        p3_after=unlocked.get('patch3') or {}
        if unlocked.get('honey') != 65 or abs(float(unlocked.get('buzzWorkMultiplier',0))-1.35)>0.001 or p3_after.get('state') != 'AVAILABLE' or p3_after.get('eligible') is not True:
            raise RuntimeError(f'Buzz purchase did not unlock gate/effect: {unlocked!r}')
        page.keyboard.press('Escape'); page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === false",timeout=timeout_ms); page.wait_for_timeout(100); _shot(page,frames/'03-world-unlocked.png')
        page.wait_for_timeout(1200)
        page.goto(_url(base_url,qa='progression_buzz_gate',qa_seed=88008,p3_storage_lifecycle='reload'),wait_until='load',timeout=timeout_ms)
        reloaded=_wait(page,head_sha,'progression_buzz_gate',timeout_ms)
        if reloaded.get('buzzLevel') != 2 or reloaded.get('honey') != 65 or (reloaded.get('patch3') or {}).get('state') != 'AVAILABLE':
            raise RuntimeError(f'Buzz/gate reload mismatch: {reloaded!r}')
        _shot(page,frames/'04-buzz-reloaded.png'); _assert_clean(console,page_errors,'P3 Buzz gate')
        return {'viewport':{'id':'desktop_reference','width':1280,'height':720},'locked':locked,'unlocked':unlocked,'reloaded':reloaded,'frame_files':[p.relative_to(output_root).as_posix() for p in sorted(frames.glob('*.png'))],'console_error_count':len(console),'page_error_count':len(page_errors)}
    finally: context.close()

def _record_mobile_panel(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict:
    frames=output_root/'p3_progression'/'mobile_landscape_frames'; context=browser.new_context(viewport={'width':844,'height':390},screen={'width':844,'height':390},device_scale_factor=1,has_touch=True,is_mobile=True)
    page=context.new_page(); console,page_errors=_errors(page)
    try:
        page.goto(_url(base_url,qa='progression_hive',qa_seed=88008),wait_until='load',timeout=timeout_ms); before=_wait(page,head_sha,'progression_hive',timeout_ms)
        # Keyboard activation is deterministic in headless mobile Chromium; pointer behavior is separately exercised by P1/P2 touch proof.
        page.keyboard.press('Space'); page.wait_for_function("() => window.__bebeeProgressionQA && window.__bebeeProgressionQA.modalOpen === true",timeout=timeout_ms); opened=_progress(page); _shot(page,frames/'00-panel.png')
        if opened.get('flightNextCost') != 30 or opened.get('buzzNextCost') != 35: raise RuntimeError(f'mobile panel data mismatch: {opened!r}')
        _assert_clean(console,page_errors,'P3 mobile panel')
        return {'viewport':{'id':'mobile_landscape','width':844,'height':390},'before':before,'opened':opened,'frame_files':[p.relative_to(output_root).as_posix() for p in sorted(frames.glob('*.png'))],'console_error_count':len(console),'page_error_count':len(page_errors)}
    finally: context.close()

def record_progression(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int) -> dict:
    desktop=_record_hive_desktop(browser,base_url=base_url,head_sha=head_sha,output_root=output_root,timeout_ms=timeout_ms)
    gate=_record_buzz_gate(browser,base_url=base_url,head_sha=head_sha,output_root=output_root,timeout_ms=timeout_ms)
    mobile=_record_mobile_panel(browser,base_url=base_url,head_sha=head_sha,output_root=output_root,timeout_ms=timeout_ms)
    return {'ticket':'P3-PROGRESSION','desktop_hive':desktop,'buzz_gate':gate,'mobile_panel':mobile,'result':'PASS'}
