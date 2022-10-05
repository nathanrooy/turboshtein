from random import choices, randint, sample
from timeit import timeit
from math import floor
import importlib
import pandas as pd


ascii = '''0123456789\
abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ\
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''


SAMPLE_SIZE = 100_00
S_LENS = [8, 16, 24, 32, 40, 48, 56]
LIBS = [
    ('jellyfish','levenshtein_distance'),
    ('Levenshtein','distance'),
    ('rapidfuzz.distance','Levenshtein.distance'),
    ('textdistance','levenshtein'),
    ('turboshtein','levenshtein'),
]


def create_strings(s_len, edit_dist):
    s1 = choices(ascii, k=s_len)
    s2 = s1[:]
    for idx in sample([i for i in range(len(s1))], edit_dist):
        s2[idx] = choices([c for c in ascii if c not in s1], k=1)[0]
    return [''.join(s1), ''.join(s2)]


funcs = []
for mname, fname in sorted(LIBS):
    module = importlib.import_module(mname)
    for _fname in fname.split('.'):
        module = getattr(module, _fname)
    funcs.append(module)

s_buf = max([len(_m) + len(_f) for _m, _f in LIBS]) + 1
df = []
for s_len in S_LENS:
    w = [create_strings(s_len, randint(0, s_len)) for _ in range(SAMPLE_SIZE)]
    for f, lib in zip(*[funcs, LIBS]):
        t = timeit(lambda: [f(w1, w2) for w1, w2 in w], number=1)
        df.append(['.'.join(lib), s_len, t])

df = pd.DataFrame(df, columns=['library', 'string_length', 'duration'])
df['pairs/sec'] = df['duration'].apply(lambda x: floor(SAMPLE_SIZE / x))
df = (
    df
    .pivot_table(
        index='library',
        columns='string_length',
        values='pairs/sec'
    )
    .reset_index()
    .sort_values(by=[8], ascending=False)
)

for s_len in S_LENS: df[s_len] = df[s_len].apply('{:,}'.format)
print(
    df.rename(columns={c:f"m=n={c}" for c in df.columns if c!='library'})
    .to_markdown(index=False, stralign="right")
)