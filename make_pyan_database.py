import os
import scipy.io

audio_dir = "primock57/output/mixed_audio"
text_dir = "primock57/output/timestamps"
out_dir = "pyan_db"

uris = []
for txt in os.listdir(text_dir):
    uris.append(txt[:-4])

print(f"total samples found: {len(uris)}")
train_f, dev_f, test_f = 0.8, 0.1, 0.1
print(f"train_f: {train_f}, dev_f: {dev_f}, test_f: {test_f}")
train_find = int(len(uris) * train_f)
dev_find = int(len(uris) * (train_f + dev_f))
train_uris = uris[: train_find]
dev_uris = uris[train_find: dev_find]
test_uris = uris[dev_find: ]
print(f"train_uris: {len(train_uris)}, dev_uris: {len(dev_uris)}, test_uris: {len(test_uris)}")

# uri list
os.mkdir(out_dir)
with open(os.path.join(out_dir, "train_list.txt"), 'w') as f:
    f.write('\n'.join(train_uris))
with open(os.path.join(out_dir, "dev_list.txt"), 'w') as f:
    f.write('\n'.join(dev_uris))
with open(os.path.join(out_dir, "test_list.txt"), 'w') as f:
    f.write('\n'.join(test_uris))

# rttms
rttm_dir = os.path.join(out_dir, "rttms")
os.mkdir(rttm_dir)
for uri in train_uris:
    with open(os.path.join(text_dir, f"{uri}.txt"), 'r') as f:
        lines = f.readlines()
    with open(os.path.join(rttm_dir, f"train_{uri}.rttm"), 'w') as f:
        for line in lines:
            st, en, spk_id = line.strip().split(",")
            spk_id = spk_id + f"_{uri}" if spk_id == "SPEAKER_01" else spk_id # if patient add uri in end for unique
            f.write(f"SPEAKER {uri} 1 {float(st):.2f} {float(en) - float(st):.2f} <NA> <NA> {spk_id} <NA> <NA>\n")
for uri in dev_uris:
    with open(os.path.join(text_dir, f"{uri}.txt"), 'r') as f:
        lines = f.readlines()
    with open(os.path.join(rttm_dir, f"dev_{uri}.rttm"), 'w') as f:
        for line in lines:
            st, en, spk_id = line.strip().split(",")
            spk_id = spk_id + f"_{uri}" if spk_id == "SPEAKER_01" else spk_id # if patient add uri in end for unique
            f.write(f"SPEAKER {uri} 1 {float(st):.2f} {float(en) - float(st):.2f} <NA> <NA> {spk_id} <NA> <NA>\n")
for uri in test_uris:
    with open(os.path.join(text_dir, f"{uri}.txt"), 'r') as f:
        lines = f.readlines()
    with open(os.path.join(rttm_dir, f"test_{uri}.rttm"), 'w') as f:
        for line in lines:
            st, en, spk_id = line.strip().split(",")
            spk_id = spk_id + f"_{uri}" if spk_id == "SPEAKER_01" else spk_id # if patient add uri in end for unique
            f.write(f"SPEAKER {uri} 1 {float(st):.2f} {float(en) - float(st):.2f} <NA> <NA> {spk_id} <NA> <NA>\n")

# uems
uem_dir = os.path.join(out_dir, "uems")
os.mkdir(uem_dir)
for uri in train_uris:
    fs, wav = scipy.io.wavfile.read(os.path.join(audio_dir, f"{uri}.wav"))
    with open(os.path.join(uem_dir, f"train_{uri}.uem"), 'w') as f:
        f.write(f"{uri} 1 0.000 {wav.shape[0] / fs}")
for uri in dev_uris:
    fs, wav = scipy.io.wavfile.read(os.path.join(audio_dir, f"{uri}.wav"))
    with open(os.path.join(uem_dir, f"dev_{uri}.uem"), 'w') as f:
        f.write(f"{uri} 1 0.000 {wav.shape[0] / fs}")
for uri in test_uris:
    fs, wav = scipy.io.wavfile.read(os.path.join(audio_dir, f"{uri}.wav"))
    with open(os.path.join(uem_dir, f"test_{uri}.uem"), 'w') as f:
        f.write(f"{uri} 1 0.000 {wav.shape[0] / fs}")
