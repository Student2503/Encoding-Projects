    #!/usr/bin/env python3

import vapoursynth as vs
import audiocutter
import lvsfunc as lvf
from subprocess import call
core = vs.core


ts_in = r"DVDISO/[DVDISO][アニメ][SHUGO CHARA!][Vol.1-16 Fin]/SHUGO_CHARA_03.d2v"
src = lvf.src(ts_in)

ac = audiocutter.AudioCutter()

if ts_in.endswith('.d2v'):
    src = core.vivtc.VFM(src, 1)
    src = core.vivtc.VDecimate(src)

vid = ac.split(src, [(71777, 106782)])

ac.ready_qp_and_chapters(vid)

vid.set_output(0)
if __name__ == "__main__":
    ac.cut_audio(r'ShuCha1DVD_09_cut.m4a', audio_source=r'DVDISO/[DVDISO][アニメ][SHUGO CHARA!][Vol.1-16 Fin]/SHUGO_CHARA_03.m4a')
