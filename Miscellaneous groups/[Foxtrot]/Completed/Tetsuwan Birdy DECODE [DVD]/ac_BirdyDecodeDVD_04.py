#!/usr/bin/env python3
import acsuite
import lvsfunc as lvf
ac = acsuite.AC()


path = r'DVDISO/(DVDISO)(アニメ) 鉄腕バーディー DECODE VOLUME03 (081126)(iso+mds+jpg)/TETSUWAN_BIRDY_03.d2v'
src = lvf.src(path)

if __name__ == "__main__":
    ac.eztrim(src, [(6450, 49008)], "DVDISO/(DVDISO)(アニメ) 鉄腕バーディー DECODE VOLUME03 (081126)(iso+mds+jpg)/TETSUWAN_BIRDY_03 Ta0 stereo 1536 kbps DELAY 0 ms.w64", "BirdyDecodeDVD_04_cut.wav")
