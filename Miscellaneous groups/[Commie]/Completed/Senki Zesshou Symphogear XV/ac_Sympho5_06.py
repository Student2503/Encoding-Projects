#!/usr/bin/env python3

import vapoursynth as vs
import audiocutter
import lvsfunc as lvf
from subprocess import call
core = vs.core

ts_in = r"src/06/Senki Zesshou Symphogear XV - 06 (BS11).d2v"
src = lvf.src(ts_in)

if ts_in.endswith(".d2v"):
    src = core.vivtc.VDecimate(src)

ac = audiocutter.AudioCutter()

vid = ac.split(src, [(682, 4806),(6485, 20773), (22212, 37845)])

ac.ready_qp_and_chapters(vid)

vid.set_output(0)
if __name__ == "__main__":
    ac.cut_audio(r'ac_Sympho5_06.aac', audio_source=r'src/06/Senki Zesshou Symphogear XV - 06 (BS11) T141 stereo 226 kbps DELAY -373 ms.aac')
