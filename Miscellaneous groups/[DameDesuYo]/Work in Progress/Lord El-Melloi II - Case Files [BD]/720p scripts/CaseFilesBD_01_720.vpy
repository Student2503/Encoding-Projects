import vapoursynth as vs
import lvsfunc as lvf
import kagefunc as kgf
import fvsfunc as fvf
import havsfunc as haf
from nnedi3_rpow2 import *
from cooldegrain import *
from vsutil import *
core = vs.core


src = lvf.src(r'BDMV/Vol 1/BDROM/BDMV/STREAM/00001.m2ts')
src = src[24:-24]
ef = core.edgefixer.ContinuityFixer(src, 1, 1, 1, 1)
ef = fvf.Depth(ef, 32)


descaled = kgf.inverse_scale(ef, height=720,
                           kernel='bicubic', b=0, c=1/2,
                           mask_detail=True)


d_mask = kgf.adaptive_grain(descaled, show_mask=True, luma_scaling=8)
denoise_a = CoolDegrain(descaled, tr=1, thsad=72, thsadc=48, bits=16, blksize=8, overlap=4)
denoise_b = CoolDegrain(descaled, tr=1, thsad=24, thsadc=48, bits=16, blksize=8, overlap=4)
denoise = core.std.MaskedMerge(denoise_a, denoise_b, fvf.Depth(d_mask, 16))

l_mask = kgf.retinex_edgemask(denoise).std.Maximum()
aa = lvf.nneedi3_clamp(denoise, mask=l_mask, strength=1.7)


d_mask = fvf.Depth(kgf.adaptive_grain(descaled, show_mask=True, luma_scaling=8), 16)
deband_a = core.f3kdb.Deband(aa, range=19, y=56, cb=48, cr=48, grainy=64, grainc=0, output_depth=16)
deband_b = core.f3kdb.Deband(aa, range=16, y=40, cb=32, cr=32, grainy=64, grainc=0, output_depth=16)
deband = core.std.MaskedMerge(deband_a, deband_b, d_mask)

grain = kgf.adaptive_grain(deband, 0.15, luma_scaling=6)


out = grain
final = fvf.Depth(out, 10)
final.set_output()