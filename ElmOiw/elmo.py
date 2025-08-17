import json
import h5py
import argparse
import torch
import numpy as np
from allennlp.modules.elmo import Elmo, batch_to_ids

def main(weights_file, options_file, raw_file, output_file):
    # Load ELMo
    elmo = Elmo(options_file, weights_file, num_output_representations=3, dropout=0)
    elmo.eval()

    # Read sentences (whitespace tokenized, one per line)
    with open(raw_file, "r", encoding="utf-8") as f:
        sentences = [line.strip().split() for line in f if line.strip()]

    # Convert to char ids
    character_ids = batch_to_ids(sentences)

    with torch.no_grad():
        embeddings = elmo(character_ids)

    # embeddings["elmo_representations"] = list of 3 tensors (layers)
    layers = [layer.cpu().numpy() for layer in embeddings["elmo_representations"]]
    mask = embeddings["mask"].cpu().numpy()

    # Save to HDF5 in AllenNLP CLI format
    with h5py.File(output_file, "w") as h5f:
        for i in range(len(sentences)):
            grp = h5f.create_group(str(i))
            sent_len = mask[i].sum()

            # Store mask
            grp.create_dataset("mask", data=mask[i][:sent_len])

            # Store each layer
            for j, layer in enumerate(layers):
                grp.create_dataset(f"layer_{j}", data=layer[i, :sent_len, :])

            # Store average layer
            avg = np.mean([layer[i, :sent_len, :] for layer in layers], axis=0)
            grp.create_dataset("average", data=avg)

            # (Optional) store tokens as attribute
            grp.attrs["tokens"] = json.dumps(sentences[i])

    print(f"✅ Saved {len(sentences)} sentences with 3 layers + average to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights_file", type=str, required=True)
    parser.add_argument("--options_file", type=str, required=True)
    parser.add_argument("--raw_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()

    main(args.weights_file, args.options_file, args.raw_file, args.output_file)
