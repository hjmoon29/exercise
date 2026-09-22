"""
Exercise 아이콘 생성 스크립트
- 원본 exercise.png에서 워터마크 제거 (밝기 threshold)
- icon-512.png, icon-192.png, favicon.png 생성
"""
from PIL import Image
from pathlib import Path
import numpy as np

PROJECT = Path(r"C:/Users/20020911/Documents/Projects/exercise")
SRC = Path(r"C:/Users/20020911/Downloads/exercise.png")
CLEAN = PROJECT / "exercise_clean.png"

src = Image.open(SRC).convert("RGB")
print("원본:", src.size)

arr = np.array(src).astype(np.int16)
gray = arr.mean(axis=2)

# 워터마크 제거:
# - 밝기 165 이상은 순수 백색으로 (워터마크 텍스트 및 밝은 아티팩트)
# - 그 이하는 원본 유지 (팔뚝 실루엣의 회색 그라데이션)
mask_bg = gray >= 165
result = arr.copy()
result[mask_bg] = [255, 255, 255]

# 팔뚝 영역 소프트닝: 근처가 워터마크로 뚫린 경우 주변 색으로 채우기 위해
# 단순화된 방식은 threshold만으로도 충분
result = np.clip(result, 0, 255).astype(np.uint8)
cleaned = Image.fromarray(result, "RGB").convert("RGBA")
cleaned.save(CLEAN)
print(f"워터마크 제거본 저장: {CLEAN.name}")

for size, name in [(512, "icon-512.png"), (192, "icon-192.png"), (32, "favicon.png")]:
    out = cleaned.resize((size, size), Image.LANCZOS)
    out.save(PROJECT / name)
    print(f"  {name}: {size}x{size}")

print("완료")
