import vapoursynth as vs
import lvsfunc as lvf
import kagefunc as kgf
import fvsfunc as fvf
import havsfunc as haf
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2
import adjust
core = vs.core

src_jp = lvf.src(r"[BDMV][Katekyou Hitman REBORN!]\[家庭教師ヒットマンREBORN！][2006][TV][BDMV][Blu-ray BOX 1][JP][20170419]\REBORN_DISC9\BDMV\STREAM\00007.m2ts")
src_jp = src_jp[:2684] # for cutting audio

src_us = lvf.src(r"REBORN CS BD\REBORN SEASONS 1-4 BD\REBORN SEASONS 1-4 D2\BDMV\STREAM\00057.m2ts")
src_us = core.std.CropRel(src_us, 4, 4, 0, 0)
src_us = core.std.AssumeFPS(src_us, fpsnum=24000, fpsden=1001)
src_us = fvf.Depth(src_us, 16)

scaled = nnedi3_rpow2(src_us)
scaled = core.resize.Spline36(scaled, 960, 720, matrix_s='709')

denoised = lvf.denoise(scaled, h=0.8)

sharp = haf.LSFmod(denoised, strength=140, soft=10, edgemode=1, Smethod=2, Lmode=2)

aa = taa.TAAmbk(sharp, aatype='Eedi3')

deband = core.f3kdb.Deband(aa, range=16, y=48, cb=40, cr=40, grainy=12, grainc=0, output_depth=16)

out = deband
final = fvf.Depth(out, 10)
final.set_output()