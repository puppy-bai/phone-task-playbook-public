#!/usr/bin/env python3
"""设备像素坐标 -> 标号截图坐标 换算。

screen detail:true 给的是设备像素（如 1080x2376），
tap_xy / gesture / input 用的是标号截图的像素（如 591x1300）。
两轴等比缩放，比例 = 截图宽 / 设备宽。

用法：
  # 1080x2376 设备屏，591x1300 截图，把设备坐标 (540, 1315) 换算过去
  python3 coords.py 1080 2376 591 1300 540 1315
  # -> 296 719

  # 也可以给多组坐标，按顺序成对输出
  python3 coords.py 1080 2376 591 1300 540 1315 843 2227

  # 反查：已知截图坐标，回推设备坐标
  python3 coords.py --back 1080 2376 591 1300 295 720
"""

import sys


def main(argv):
    args = list(argv)
    back = False
    if args and args[0] == "--back":
        back = True
        args = args[1:]

    if len(args) < 4:
        print(__doc__)
        return 1

    try:
        dw, dh, sw, sh = (float(v) for v in args[:4])
        rest = [float(v) for v in args[4:]]
    except ValueError:
        print("参数必须是数字：<设备W> <设备H> <截图W> <截图H> [x y]...", file=sys.stderr)
        return 1

    if dw <= 0 or dh <= 0 or sw <= 0 or sh <= 0:
        print("宽高必须为正数", file=sys.stderr)
        return 1
    if rest and len(rest) % 2:
        print("坐标要成对给：x y x y ...", file=sys.stderr)
        return 1

    kx, ky = sw / dw, sh / dh
    if back:
        kx, ky = 1 / kx, 1 / ky
        label = "截图 -> 设备"
    else:
        label = "设备 -> 截图"

    if not rest:
        print("比例 %.4f (x) / %.4f (y)  [%s]" % (kx, ky, label))
        return 0

    for i in range(0, len(rest), 2):
        x, y = rest[i] * kx, rest[i + 1] * ky
        print("%d %d" % (round(x), round(y)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
