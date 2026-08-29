#!/usr/bin/env python3
"""Exercise BeBee movement, pollination and progression in real Chromium."""
from __future__ import annotations
import argparse, hashlib, json, math, tempfile, time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from playwright.sync_api import Browser, Page, sync_playwright
from capture_pollination_qa import record_pollination_core
from capture_progression_qa import record_progression

def sha256_file(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b''): digest.update(chunk)
    return digest.hexdigest()

def with_query(base_url: str, **values: object) -> str:
    parsed=urlsplit(base_url); query=dict(parse_qsl(parsed.query,keep_blank_values=True))
    for key,value in values.items(): query[key]=str(value)
    return urlunsplit((parsed.scheme,parsed.netloc,parsed.path,urlencode(query),parsed.fragment))

def bridge(page: Page) -> dict[str,object]:
    value=page.evaluate("() => window.__bebeeMovementQA ? structuredClone(window.__bebeeMovementQA) : null")
    if not isinstance(value,dict): raise RuntimeError('window.__bebeeMovementQA is not available')
    for field in ('beeX','beeY','speed','cameraX','cameraY','distanceTravelled','frame'):
        fv=value.get(field)
        if not isinstance(fv,(int,float)) or not math.isfinite(float(fv)): raise RuntimeError(f'Movement bridge field {field} is not finite: {value!r}')
    return value

def install_error_capture(page: Page):
    console_errors=[]; page_errors=[]
    page.on('console',lambda message:console_errors.append(message.text) if message.type in {'error','assert'} else None)
    page.on('pageerror',lambda error:page_errors.append(str(error)))
    return console_errors,page_errors

def wait_ready(page: Page, *, head_sha: str, state_id: str, timeout_ms: int):
    page.wait_for_function("() => window.__bebeeQA && window.__bebeeQA.captureReady === true && !!window.__bebeeMovementQA",timeout=timeout_ms)
    qa=page.evaluate("() => structuredClone(window.__bebeeQA)")
    if qa.get('stateId') != state_id or qa.get('buildCommitSha') != head_sha: raise RuntimeError(f'movement QA provenance mismatch: {qa!r}')
    return bridge(page)

def assert_no_errors(console_errors,page_errors,label):
    if console_errors or page_errors: raise RuntimeError(f'{label}: console={console_errors!r} page={page_errors!r}')

def screenshot(page: Page,path: Path):
    path.parent.mkdir(parents=True,exist_ok=True); page.screenshot(path=str(path),full_page=False,animations='disabled')

def record_desktop_motion(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int):
    frames=output_root/'movement_dense'/'desktop_reference_frames'; video_path=output_root/'movement_dense'/'desktop_reference.webm'; video_path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='bebee-movement-desktop-') as video_dir:
        context=browser.new_context(viewport={'width':1280,'height':720},screen={'width':1280,'height':720},device_scale_factor=1,record_video_dir=video_dir,record_video_size={'width':1280,'height':720})
        page=context.new_page(); video=page.video; console_errors,page_errors=install_error_capture(page)
        try:
            page.goto(with_query(base_url,qa='movement_dense',qa_seed=88008),wait_until='load',timeout=timeout_ms)
            start=wait_ready(page,head_sha=head_sha,state_id='movement_dense',timeout_ms=timeout_ms); screenshot(page,frames/'00-idle.png'); t0=time.monotonic()
            page.keyboard.down('d'); page.wait_for_timeout(350); early=bridge(page); screenshot(page,frames/'01-accelerating.png')
            page.wait_for_timeout(500); cruise=bridge(page); screenshot(page,frames/'02-cruise.png')
            page.keyboard.down('w'); page.wait_for_timeout(650); diagonal=bridge(page); screenshot(page,frames/'03-diagonal.png')
            page.keyboard.up('w'); page.keyboard.up('d'); page.wait_for_timeout(450); stopped=bridge(page); screenshot(page,frames/'04-stopped.png'); duration=time.monotonic()-t0
            if early.get('inputSource')!='keyboard' or float(early['speed'])<=100: raise RuntimeError(f'desktop keyboard did not accelerate: {early!r}')
            if float(cruise['beeX'])-float(start['beeX'])<=80: raise RuntimeError(f'desktop displacement too small: start={start!r} cruise={cruise!r}')
            if not 250<=float(cruise['speed'])<=305: raise RuntimeError(f'desktop cruise speed outside band: {cruise!r}')
            if diagonal.get('inputSource')!='keyboard' or abs(math.hypot(float(diagonal['intentX']),float(diagonal['intentY']))-1)>0.02: raise RuntimeError(f'desktop diagonal intent invalid: {diagonal!r}')
            if float(stopped['speed'])>5 or stopped.get('inputSource')!='none': raise RuntimeError(f'desktop release did not settle: {stopped!r}')
            if int(stopped.get('boundHits',0))!=0: raise RuntimeError(f'desktop central proof hit bounds: {stopped!r}')
            observed_frames=int(stopped['frame'])-int(start['frame']); observed_fps=observed_frames/max(duration,0.001)
            if observed_fps<20 or not 2.0<=duration<=6.0: raise RuntimeError(f'desktop runtime timing invalid: fps={observed_fps:.2f} duration={duration:.3f}')
            assert_no_errors(console_errors,page_errors,'desktop movement')
            result={'viewport':{'id':'desktop_reference','width':1280,'height':720},'exercise_seconds':round(duration,3),'observed_frames':observed_frames,'observed_fps':round(observed_fps,2),'start':start,'early':early,'cruise':cruise,'diagonal':diagonal,'stopped':stopped,'console_error_count':len(console_errors),'page_error_count':len(page_errors)}
        finally: context.close()
        if video is None: raise RuntimeError('desktop movement video handle missing')
        video.save_as(str(video_path))
    if not video_path.is_file() or video_path.stat().st_size==0: raise RuntimeError('desktop movement video missing')
    result['video_file']=video_path.relative_to(output_root).as_posix(); result['video_sha256']=sha256_file(video_path); result['frame_files']=[p.relative_to(output_root).as_posix() for p in sorted(frames.glob('*.png'))]
    return result

def dispatch_touch(session,event_type,points): session.send('Input.dispatchTouchEvent',{'type':event_type,'touchPoints':points})

def record_touch_motion(browser: Browser, *, base_url: str, head_sha: str, output_root: Path, timeout_ms: int):
    frames=output_root/'movement_dense'/'mobile_landscape_frames'; video_path=output_root/'movement_dense'/'mobile_landscape.webm'; video_path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='bebee-movement-touch-') as video_dir:
        context=browser.new_context(viewport={'width':844,'height':390},screen={'width':844,'height':390},device_scale_factor=1,has_touch=True,is_mobile=True,record_video_dir=video_dir,record_video_size={'width':844,'height':390})
        page=context.new_page(); video=page.video; console_errors,page_errors=install_error_capture(page); session=context.new_cdp_session(page); session.send('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':1})
        try:
            page.goto(with_query(base_url,qa='movement_dense',qa_seed=88008),wait_until='load',timeout=timeout_ms); start=wait_ready(page,head_sha=head_sha,state_id='movement_dense',timeout_ms=timeout_ms); screenshot(page,frames/'00-idle.png')
            anchor={'x':170,'y':210,'radiusX':1,'radiusY':1,'force':1,'id':1}; right={'x':290,'y':210,'radiusX':1,'radiusY':1,'force':1,'id':1}; diag={'x':275,'y':125,'radiusX':1,'radiusY':1,'force':1,'id':1}; t0=time.monotonic()
            dispatch_touch(session,'touchStart',[anchor]); page.wait_for_timeout(250); dispatch_touch(session,'touchMove',[right]); page.wait_for_timeout(500); active=bridge(page); screenshot(page,frames/'01-horizontal.png')
            page.wait_for_timeout(400); dispatch_touch(session,'touchMove',[diag]); page.wait_for_timeout(500); diagonal=bridge(page); screenshot(page,frames/'02-diagonal.png'); dispatch_touch(session,'touchEnd',[]); page.wait_for_timeout(500); stopped=bridge(page); screenshot(page,frames/'03-stopped.png'); duration=time.monotonic()-t0
            if active.get('inputSource')!='touch' or float(active['speed'])<=100: raise RuntimeError(f'touch movement did not activate: {active!r}')
            if float(active['beeX'])-float(start['beeX'])<=50: raise RuntimeError(f'touch displacement too small: {active!r}')
            touch_intent=math.hypot(float(diagonal['intentX']),float(diagonal['intentY']))
            if diagonal.get('inputSource')!='touch' or touch_intent<=0.4 or touch_intent>1.02: raise RuntimeError(f'touch diagonal intent invalid: {diagonal!r}')
            if float(stopped['speed'])>5 or stopped.get('inputSource')!='none': raise RuntimeError(f'touch release did not settle: {stopped!r}')
            assert_no_errors(console_errors,page_errors,'touch movement')
            result={'viewport':{'id':'mobile_landscape','width':844,'height':390},'exercise_seconds':round(duration,3),'start':start,'active':active,'diagonal':diagonal,'stopped':stopped,'console_error_count':len(console_errors),'page_error_count':len(page_errors)}
        finally: context.close()
        if video is None: raise RuntimeError('touch movement video handle missing')
        video.save_as(str(video_path))
    if not video_path.is_file() or video_path.stat().st_size==0: raise RuntimeError('touch movement video missing')
    result['video_file']=video_path.relative_to(output_root).as_posix(); result['video_sha256']=sha256_file(video_path); result['frame_files']=[p.relative_to(output_root).as_posix() for p in sorted(frames.glob('*.png'))]
    return result

def dispatch_escape(session,page: Page):
    common={'windowsVirtualKeyCode':27,'nativeVirtualKeyCode':27}; page.wait_for_timeout(40); session.send('Input.dispatchKeyEvent',{'type':'rawKeyDown',**common}); page.wait_for_timeout(80); session.send('Input.dispatchKeyEvent',{'type':'keyUp',**common}); page.wait_for_timeout(80)

def verify_modal_and_reduced_motion(browser: Browser, *, base_url: str, head_sha: str, timeout_ms: int):
    context=browser.new_context(viewport={'width':1280,'height':720},screen={'width':1280,'height':720},device_scale_factor=1); page=context.new_page(); session=context.new_cdp_session(page); console_errors,page_errors=install_error_capture(page); console_lines=[]; page.on('console',lambda message:console_lines.append(message.text))
    try:
        page.goto(with_query(base_url,qa='movement_empty',qa_seed=88008,reduced_motion=1),wait_until='load',timeout=timeout_ms); start=wait_ready(page,head_sha=head_sha,state_id='movement_empty',timeout_ms=timeout_ms)
        if start.get('reducedMotion') is not True: raise RuntimeError(f'reduced motion override missing: {start!r}')
        page.keyboard.down('d'); page.wait_for_timeout(700); moving=bridge(page); page.keyboard.up('d'); page.wait_for_timeout(300); lag_x=abs(float(moving['beeX'])-float(moving['cameraX'])); lag_y=abs(float(moving['beeY'])-float(moving['cameraY']))
        if lag_x>0.1 or lag_y>0.1: raise RuntimeError(f'reduced-motion camera lagged: {moving!r}')
        dispatch_escape(session,page)
        if not any('BEBEE_INPUT modal_open focus_acquired' in line for line in console_lines): raise RuntimeError(f'modal did not acquire focus: {console_lines!r}')
        before_modal=bridge(page); page.keyboard.down('d'); page.wait_for_timeout(550); page.keyboard.up('d'); page.wait_for_timeout(250); after_modal=bridge(page); displacement=abs(float(after_modal['beeX'])-float(before_modal['beeX']))
        if displacement>1.0: raise RuntimeError(f'movement leaked through modal: {before_modal!r} -> {after_modal!r}')
        dispatch_escape(session,page)
        if not any('BEBEE_INPUT modal_closed focus_released' in line for line in console_lines): raise RuntimeError(f'modal did not release focus: {console_lines!r}')
        assert_no_errors(console_errors,page_errors,'modal/reduced-motion')
        return {'reduced_motion_applied':True,'camera_lag_abs_x':round(lag_x,4),'camera_lag_abs_y':round(lag_y,4),'modal_displacement':round(displacement,4),'modal_focus_consumed_movement':True,'console_error_count':len(console_errors),'page_error_count':len(page_errors)}
    finally: context.close()

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument('--head-sha',required=True); parser.add_argument('--url',default='http://127.0.0.1:8000/development/BeBee/'); parser.add_argument('--output-root',type=Path,required=True); parser.add_argument('--timeout-seconds',type=int,default=20); args=parser.parse_args()
    head_sha=args.head_sha.strip().lower()
    if len(head_sha)!=40 or any(ch not in '0123456789abcdef' for ch in head_sha): raise RuntimeError('--head-sha must be a full 40-character Git SHA')
    output_root=args.output_root.expanduser().resolve(); output_root.mkdir(parents=True,exist_ok=True); timeout_ms=args.timeout_seconds*1000
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        try:
            desktop=record_desktop_motion(browser,base_url=args.url,head_sha=head_sha,output_root=output_root,timeout_ms=timeout_ms)
            touch=record_touch_motion(browser,base_url=args.url,head_sha=head_sha,output_root=output_root,timeout_ms=timeout_ms)
            safety=verify_modal_and_reduced_motion(browser,base_url=args.url,head_sha=head_sha,timeout_ms=timeout_ms)
            pollination=record_pollination_core(browser,base_url=args.url,head_sha=head_sha,output_root=output_root,timeout_ms=timeout_ms)
            progression=record_progression(browser,base_url=args.url,head_sha=head_sha,output_root=output_root,timeout_ms=timeout_ms)
            browser_version=browser.version
        finally: browser.close()
    report={'schema_version':2,'ticket':'P1-BEE-MOVEMENT','head_sha':head_sha,'browser_name':'Playwright Chromium','browser_version':browser_version,'qa_seed':88008,'desktop_keyboard':desktop,'mobile_touch':touch,'focus_and_accessibility':safety,'p2_pollination_core':pollination,'p3_progression':progression,'result':'PASS'}
    report_path=output_root/'motion-report.json'; report_path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f"P1 movement + P2 pollination + P3 progression browser proof: PASS (desktop movement {desktop['exercise_seconds']}s, touch movement {touch['exercise_seconds']}s, desktop movement {desktop['observed_fps']} fps, P2={pollination['result']}, P3={progression['result']})")
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,RuntimeError,ValueError) as exc:
        print(f'Movement/P2/P3 browser proof failed: {exc}'); raise SystemExit(1)
