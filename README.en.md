Lexide Toolchain: [LEXIDE-Ω development tools](http://rohmfs-rohm-com-cn.oss-cn-shanghai.aliyuncs.com/lapis/support/lpmcu/DL_DATA/DEV_TOOL/soft_tool/U8_Development_Tools/LAPIS_LEXIDE_V1_1_1.zip)

gitee/github Repository: [gitee](http://gitee.com/mc-sdx/calcracker) , [github](http://github.com/mc-sdx/CWI-hacking/tree/master)

uEASE New Version Firmware: [uEase V3.21](http://rohmfs-rohm-com-cn.oss-cn-shanghai.aliyuncs.com/lapis/support/lpmcu/DL_DATA/DEV_TOOL/soft_tool/MWuEASE/uEASE_Firmware_Ver321.zip), or in my repository.

## Preparation:
1. Install the Lexide toolchain first.
2. In the installation directory, locate the ML620418.TRG file and replace it with the TRG file from my repository.
3. Remove the calculator battery and connect the calculator to uEASE.
4. CALC and uEASE connections:
   - P152 — SDA
   - P151 — SCK
   - P150(reversed)
   - (reversed)VPP
   - VCC — 3.3V, VREF (connect together to the calculator VCC)
   - GND — GND
uEASE Pinout

#＃ Update uEASE:
Open dtu8, click on "update," then click on the "ueb" icon at the top left corner, select the firmware, and click OK.