#!/usr/bin/env python3

import vapoursynth as vs
import audiocutter
from subprocess import call


core = vs.core
ts_in = r"BDMV/[BDMV][アニメ][171227] 「終物語」 第八巻／おうぎダーク/BD_VIDEO/BDMV/STREAM/00010.m2ts"
src = core.lsmas.LWLibavSource(ts_in)

ac = audiocutter.AudioCutter()

vid = ac.split(src, [(12,2171)])

ac.ready_qp_and_chapters(vid)

vid.set_output(0)
if __name__ == "__main__":
    ac.cut_audio(r'Owari2BD_NCOP3_cut.m4a', audio_source=r'BDMV/[BDMV][アニメ][171227] 「終物語」 第八巻／おうぎダーク/BD_VIDEO/BDMV/STREAM/00010.m4a')
