from math import floor
from random import randint
from timeit import repeat
import importlib
import pandas as pd
from utils import create_strings


SAMPLE_SIZE = 10_000
S_LENS = [8, 16, 24, 32, 40, 48, 56]
LIBS = [
    ('jellyfish','levenshtein_distance'),
    ('Levenshtein','distance'),
    ('rapidfuzz.distance','Levenshtein.distance'),
    ('textdistance','levenshtein'),
    ('turboshtein','levenshtein'),
]


funcs = []
for mname, fname in LIBS:
    module = importlib.import_module(mname)
    for _fname in fname.split('.'):
        module = getattr(module, _fname)
    funcs.append(module)

s_buf = max([len(_m) + len(_f) for _m, _f in LIBS]) + 1
df = []
for s_len in S_LENS:
    w = [create_strings(s_len, randint(0, s_len)) for _ in range(SAMPLE_SIZE)]
    for f, lib in zip(*[funcs, LIBS]):
        t = repeat(lambda: [f(w1, w2) for w1, w2 in w], repeat=1_000, number=1)
        df.append(['.'.join(lib), s_len, min(t)])

df = pd.DataFrame(df, columns=['library', 'string_length', 'duration'])
df['pairs/sec'] = df['duration'].apply(lambda x: floor(SAMPLE_SIZE / x))
df = (
    df.pivot_table(index='library', columns='string_length', values='pairs/sec')
    .reset_index()
    .sort_values(by=[8], ascending=False)
)

for s_len in S_LENS: df[s_len] = df[s_len].apply('{:,}'.format)
print(
    df.rename(columns={c:f"m=n={c}" for c in df.columns if c!='library'})
    .to_markdown(index=False, stralign="right")
)
