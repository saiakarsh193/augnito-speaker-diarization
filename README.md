### To install the environment
```bash
conda create --prefix ./augnito python=3.9
conda activate ./augnito
./augnito/bin/python3 -m pip install -r requirements.txt
```

### To install and prepare the dataset
```bash
git clone https://github.com/babylonhealth/primock57
cd primock57/scripts/
bash mix_audio.sh
```

make the following changes in `textgrid_to_transcript.py` (inside `primock57/scripts/`)
```python
# line 15, from this
return [f"{u['speaker']}: {strip_transcript_tags(u['text'])}"
            for u in combined_utterances]
# to
return [f"{u['from']}::{u['to']}::{u['speaker']}::{strip_transcript_tags(u['text'])}"
            for u in combined_utterances]
```

```bash
python3 textgrid_to_transcript.py --transcript_path ../transcripts --output_path ../output/joined_transcripts
cd ../../ # go to home dir
python3 transcript_to_timestamps.py # to convert the joined_transcripts into timestamps
```
*NOTE:* Doctor is SPEAKER_00 and patient is SPEAKER_01 in the timestamps

### To prepare pyannote dataset
We need to create a `pyannote.dataset` using the above dataset for finetuning the model.

```bash
python3 make_pyan_database.py # will create necessary files in pyan_db directory
```

Create a file `database.yml` in the home dir, and add the following
```yaml
Databases:
  Primock: primock57/output/mixed_audio/{uri}.wav

Protocols:
  Primock:
    SpeakerDiarization:
      full:
        train:
            uri: pyan_db/train_list.txt
            annotation: pyan_db/rttms/train_{uri}.rttm
            annotated: pyan_db/uems/train_{uri}.uem
        development:
            uri: pyan_db/dev_list.txt
            annotation: pyan_db/rttms/dev_{uri}.rttm
            annotated: pyan_db/uems/dev_{uri}.uem
        test:
            uri: pyan_db/test_list.txt
            annotation: pyan_db/rttms/test_{uri}.rttm
            annotated: pyan_db/uems/test_{uri}.uem
```

To check if the `pyannote.dataset` was created properly
```bash
python3 check_protocol.py
```

### How to run
`pyan_finetune.ipynb` has the code to finetune the SpeakerDiarization model using `pyannote/speaker-diarization-3.1` and `pyannote/segmentation-3.0`. It uses the created `database.yml` `pyannote.dataset` to do this.

`pyan_inf.ipynb` will run inference on the dataset using both the pretrained and finetuned models and create the output directories `timestamps_pyan_diar_pretrained` and `timestamps_pyan_diar_pretrained`.

`nemo_inf.ipynb` will run inference on the dataset using pretrained`marblenet-vad`, `titanet_large-speaker_embedder` and creates the output directory `timestamps_nemo_pretrained`.

`der.ipynb` has the code to calculate Diarization Error Rate (DER) for all the models used.