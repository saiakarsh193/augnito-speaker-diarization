import os

src_dir = "primock57/output/joined_transcripts"
out_dir = "primock57/output/timestamps"
os.mkdir(out_dir)

for txt in os.listdir(src_dir):
    txt_path = os.path.join(src_dir, txt)
    with open(txt_path, 'r') as f:
        lines = f.readlines()
    with open(os.path.join(out_dir, txt), 'w') as f:
        for line in lines:
            st, en, spk = line.strip().split("::")[:3]
            spk_id = "SPEAKER_00" if spk == "Doctor" else "SPEAKER_01"
            f.write(f"{float(st):.3f},{float(en):.3f},{spk_id}\n")
