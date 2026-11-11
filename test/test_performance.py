import importlib
import importlib.metadata
import sys
from math import floor
from random import randint
from timeit import repeat

import pandas as pd

from test.utils import create_strings

SAMPLE_SIZE = 10_000
REPEAT = 50
S_LENS = [8, 16, 24, 32, 40, 48, 56]
LIBS = [
    ("turboshtein", "levenshtein"),
    ("rapidfuzz.distance", "Levenshtein.distance"),
    ("Levenshtein", "distance"),
    ("jellyfish", "levenshtein_distance"),
    ("textdistance", "levenshtein"),
]

versions = {}
for mname, _ in LIBS:
    pkg = mname.split(".")[0]
    mod = importlib.import_module(pkg)
    ver = getattr(mod, "__version__", None)
    if ver is None:
        ver = importlib.metadata.version(pkg)
    versions[mname] = ver

funcs = []
for mname, fname in LIBS:
    module = importlib.import_module(mname)
    for _fname in fname.split("."):
        module = getattr(module, _fname)
    funcs.append(module)

rows = []
for s_len in S_LENS:
    print(f"Benchmarking length m=n={s_len}...", file=sys.stderr, flush=True)
    w = [create_strings(s_len, randint(0, s_len)) for _ in range(SAMPLE_SIZE)]
    for (mname, fname), f in zip(LIBS, funcs, strict=True):
        full_name = f"{mname}.{fname}" if mname != fname else fname
        t = repeat(
            lambda _f=f, _w=w: [_f(w1, w2) for w1, w2 in _w],
            repeat=REPEAT,
            number=1,
        )
        rate = floor(SAMPLE_SIZE / min(t))
        rows.append(
            {
                "library": full_name,
                "length": s_len,
                "rate": rate,
                "version": versions[mname],
            }
        )

df = pd.DataFrame(rows)
turbo_rates = (
    df[df["library"] == "turboshtein.levenshtein"].set_index("length")["rate"].to_dict()
)


def calc_advantage(lib_name: str) -> str:
    if "turboshtein" in lib_name:
        return "baseline"
    lib_df = df[df["library"] == lib_name]
    multipliers = [
        turbo_rates[len_] / rate
        for len_, rate in zip(lib_df["length"], lib_df["rate"], strict=True)
    ]
    low, high = min(multipliers), max(multipliers)
    if high >= 10:
        return f"**{low:.0f}x – {high:.0f}x faster**"  # noqa: RUF001
    return f"**{low:.1f}x – {high:.1f}x faster**"  # noqa: RUF001


df["formatted"] = df["rate"].apply(lambda x: f"{x:,}")
pivot = df.pivot(
    index=["library", "version"], columns="length", values="formatted"
).reset_index()

pivot["turboshtein advantage"] = pivot["library"].apply(calc_advantage)

order = {
    "turboshtein.levenshtein": 0,
    "rapidfuzz.distance.Levenshtein.distance": 1,
    "Levenshtein.distance": 2,
    "jellyfish.levenshtein_distance": 3,
    "textdistance.levenshtein": 4,
}
pivot["rank"] = pivot["library"].map(order)
pivot = pivot.sort_values("rank").drop(columns=["rank"])

headers = ["library", "version", "turboshtein advantage"] + [
    f"m=n={slen}" for slen in S_LENS
]
lines = [
    "| " + " | ".join(headers) + " |",
    "| " + " | ".join(["---:", "---:", ":---:"] + ["---:"] * len(S_LENS)) + " |",
]
for _, row in pivot.iterrows():
    lib = row["library"]
    if "Levenshtein." in lib and "rapidfuzz" not in lib:
        lib = "[Levenshtein.distance](https://github.com/rapidfuzz/Levenshtein)"
    elif "rapidfuzz" in lib:
        lib = "[rapidfuzz.distance.Levenshtein.distance](https://github.com/rapidfuzz/RapidFuzz)"
    elif "jellyfish" in lib:
        lib = "[jellyfish.levenshtein_distance](https://github.com/jamesturk/jellyfish)"
    elif "textdistance" in lib:
        lib = "[textdistance.levenshtein](https://github.com/life4/textdistance)"
    val_strs = [lib, str(row["version"]), str(row["turboshtein advantage"])] + [
        str(row[slen]) for slen in S_LENS
    ]
    lines.append("| " + " | ".join(val_strs) + " |")

print("\n".join(lines))
