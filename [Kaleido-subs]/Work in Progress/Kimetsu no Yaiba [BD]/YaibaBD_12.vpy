import vapoursynth as vs
import fvsfunc as fvf
import kagefunc as kgf
import lvsfunc as lvf
import mvsfunc as mvf
from cooldegrain import *
from knnfunc import *
from nnedi3_rpow2 import *
from vsutil import *
core = vs.core

opstart, edstart = 2805-2159, 33086-2159

# There are some frames with stylized dark background and slow-motion effects.
# They be will filtered slightly stronger than other scenes, and heavily grained because I like the look.
darker_shots = """
               [14330 14344]
               [14434 14436]
               [29972 30085]
               """


src = lvf.src(r"BDMV/[BDMV][191127][Kimetsu no Yaiba][Vol.5]/BDMV/STREAM/00005.m2ts")
src = src[:-25]
src = fvf.Depth(src, 16)


b, c = 1/5, 2/5
y, u, v = split(src)
# Descaling & create credit mask
descaled = core.descale.Debicubic(fvf.Depth(y, 32), get_w(855), 855, b, c)
upscaled = core.resize.Bicubic(descaled, y.width, y.height, filter_param_a=b, filter_param_b=c)
credit_mask = core.std.Expr([fvf.Depth(y, 32), upscaled], 'x y - abs').std.Binarize(0.05)
credit_mask = kgf.iterate(credit_mask, core.std.Maximum, 6)
credit_mask = kgf.iterate(credit_mask, core.std.Inflate, 2)

# waifu2x to fix up two frames in the OP with very bad noise
w2x = mvf.ToYUV(core.w2xc.Waifu2x(mvf.ToRGB(descaled), noise=1, scale=1, gpu=0)).resize.Point(format=descaled.format)
w2x = fvf.rfs(descaled, w2x, mappings=f"{opstart+1593} {opstart+1594}")

# Fairly weak denoising. Stronger denoising on brighter areas of a frame.
# Done while descaled because it's overall faster *and* more effective.
d_mask = kgf.adaptive_grain(fvf.Depth(descaled, 16), show_mask=True, luma_scaling=8)
denoise_a = CoolDegrain(w2x, tr=1, thsad=72, thsadc=48, bits=16, blksize=8, overlap=4)
denoise_b = CoolDegrain(w2x, tr=1, thsad=24, thsadc=48, bits=16, blksize=8, overlap=4)
denoise = core.std.MaskedMerge(denoise_a, denoise_b, d_mask)
denoise = fvf.rfs(denoise, denoise_a, mappings=f"""[{opstart+28} {opstart+288}] [{opstart+401} {opstart+406}] [{opstart+1310} {opstart+1398}]
                                                   """)

# Some AA to fix up instances of bad lineart.
# Done while descaled for similar reasons as L37
aa_a = lvf.upscaled_sraa(denoise)
aa_b = knnAA(denoise)
aa = fvf.rfs(denoise, aa_a, mappings=f"""[{opstart+1017} {opstart+1079}] [{opstart+1312} {opstart+1368}] {opstart+1593} {opstart+1594} [{opstart+1895} {opstart+2003}]
                                         [{edstart+890} {edstart+1032}]""")
aa = fvf.rfs(aa, aa_b, mappings=darker_shots)

# Upscaling and applying credit mask to OP and ED
upscaled = nnedi3_rpow2(aa).resize.Bicubic(src.width, src.height)
upscaled = join([upscaled, u, v])
m_upscaled = core.std.MaskedMerge(upscaled, src, fvf.Depth(credit_mask, 16))
scaled = fvf.rfs(upscaled, m_upscaled, mappings=f"[{opstart} {opstart+2159}] [{edstart} {edstart+2159}]")


# Much like the denoising, way stronger debanding is performed on brighter areas.
# This way less perceivable detail is lost to the void. Darker areas will be grained stronger instead.
deb_d_mask = fvf.Depth(kgf.adaptive_grain(src, show_mask=True, luma_scaling=8), 16)
deband_a = core.f3kdb.Deband(scaled, range=21, y=56, cb=48, cr=48, grainy=12, grainc=0, output_depth=16)
deband_b = core.f3kdb.Deband(scaled, range=17, y=40, cb=32, cr=32, grainy=24, grainc=0, output_depth=16)
deband = core.std.MaskedMerge(deband_a, deband_b, deb_d_mask)
deband = fvf.rfs(deband, deband_a, mappings=darker_shots +
                                            f"""[{opstart+2004} {opstart+2046}] [{opstart+2113} {opstart+2156}]
                                                [{edstart+1494} {edstart+1600}]
                                                """)

# Graining. Strong dynamic grain added to parts of the OP and darker slow-motion scenes.
grain_a = kgf.adaptive_grain(deband, 0.3, luma_scaling=8)
grain_b = kgf.adaptive_grain(deband, 1)
grain_c = core.grain.Add(deband, var=6, uvar=0, constant=False)
grain_d = core.grain.Add(deband, var=3, uvar=0, constant=False)
grain = fvf.rfs(grain_a, grain_b, mappings=f"""[{opstart+1128} {opstart+1296}] [{opstart+2004} {opstart+2046}] [{opstart+2113} {opstart+2156}]
                                               """)
grain = fvf.rfs(grain, grain_c, mappings=f"[{opstart+28} {opstart+288}] [{opstart+401} {opstart+406}] [{opstart+1313} {opstart+1368}]")
grain = fvf.rfs(grain, grain_d, mappings=darker_shots)


out = grain
final = fvf.Depth(out, 10)
final.set_output()
