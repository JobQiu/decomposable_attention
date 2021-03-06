import numpy as np
from data.base_sequence_data import BaseSequenceData


class PairSequenceData(BaseSequenceData):
    """
    Pair sequence data class interface for
    decomposable attention classification model
    """
    def __init__(self):
        """
        Data format should be [(sequence1, sequence2, label)]
        """
        super(PairSequenceData, self).__init__()

    def _next_batch(self, data, batch_idxs):
        """
        Generate next batch.
        :param data: data list to process
        :param batch_idxs: idxs to process
        :return: next data dict of batch_size amount data
        """
        def _normalize_length(_data, max_length):
            return _data + [self.PAD] * (max_length - len(_data))

        seq1_data, seq1_lengths, seq2_data, seq2_lengths, labels = \
            [], [], [], [], []
        for idx in batch_idxs:
            seq1, seq2, _ = data[idx]
            seq1_lengths.append(len(seq1))
            seq2_lengths.append(len(seq2))

        seq1_max_length = max(seq1_lengths)
        seq2_max_length = max(seq2_lengths)
        for idx in batch_idxs:
            seq1, seq2, label = data[idx]
            seq1_data.append(_normalize_length(seq1, seq1_max_length))
            seq2_data.append(_normalize_length(seq2, seq2_max_length))
            labels.append(label)

        batch_data_dict = {
            'sentence1_inputs': np.asarray(seq1_data, dtype=np.int32),
            'sentence1_lengths': np.asarray(seq1_lengths, dtype=np.int32),
            'sentence2_inputs': np.asarray(seq2_data, dtype=np.int32),
            'sentence2_lengths': np.asarray(seq2_lengths, dtype=np.int32),
            'labels': np.asarray(labels, dtype=np.int32)
        }
        return batch_data_dict

    def build(self):
        """
        Build data and save in self.train_sequences, self.val_sequences
        """
        raise NotImplementedError

    def load(self):
        """
        Load data and save in self.train_sequences, self.val_sequences
        """
        raise NotImplementedError