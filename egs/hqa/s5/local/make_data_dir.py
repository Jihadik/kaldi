from __future__ import print_function

import argparse
import os
import codecs


def mkdir_recursive(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def parse_arguments():
    description = \
      'Takes a path to the directory containing coupled .txt and .wav files\n' \
      '(possibly in a nested structure) and the output dir name in data/\n' \
      'Outputs files: wav.scp, text, utt2spk, spk2utt, spk2gender'
    parser = argparse.ArgumentParser(description)
    parser.add_argument('srcdir', type=str, help='Directory with source data')
    parser.add_argument('destdir', type=str, help='Destination directory')

    args = parser.parse_args()
    return args


def main(srcdir, destdir):
    if not os.path.exists(srcdir):
        print('No such directory {}'.format(srcdir))
        return
    mkdir_recursive(destdir)

    wav = []
    text = []
    utt2spk = []
    spk2utt = []
    spk2gender = []
    for root, subFolders, files in os.walk(srcdir):
        spk = os.path.basename(os.path.normpath(root))
        utts = []
        for file in files:
            file_name = os.path.abspath(os.path.join(root, file))
            utt = 'SPEAKER-{}-UTT-{}'.format(spk, file[:-4])
            if file.endswith('.txt'):
                text.append(u'{} {}'.format(utt, codecs.open(file_name, 'r', 'utf-8').read()))
            elif file.endswith('.wav'):
                wav.append('{} {}'.format(utt, file_name))
                utt2spk.append('{} {}'.format(utt, spk))
                utts.append(utt)
        if len(utts) != 0:
            spk2utt.append('{} {}'.format(spk, ' '.join(utts)))
            if 'male' in spk: # Not the best way
                spk2gender.append('{} m'.format(spk))
            else:
                spk2gender.append('{} f'.format(spk))

    with codecs.open(os.path.join(destdir, 'text'), 'w', 'utf-8') as fout:
        fout.write(''.join(text))
    with open(os.path.join(destdir, 'wav.scp'), 'w') as fout:
        fout.write('\n'.join(wav) + '\n')
    with open(os.path.join(destdir, 'utt2spk'), 'w') as fout:
        fout.write('\n'.join(utt2spk) + '\n')
    with open(os.path.join(destdir, 'spk2utt'), 'w') as fout:
        fout.write('\n'.join(spk2utt) + '\n')
    with open(os.path.join(destdir, 'spk2gender'), 'w') as fout:
        fout.write('\n'.join(spk2gender) + '\n')

if __name__ == "__main__":
    args = parse_arguments()
    main(**vars(args))

