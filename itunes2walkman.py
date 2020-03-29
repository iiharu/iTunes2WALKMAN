#!/usr/bin/env python

from __future__ import print_function

import argparse
import itertools
import plistlib
import shutil
import os
import urllib
from tqdm import tqdm


def load(args):
    # type: (argparse.Namespace) -> str, Dict[int, str], Dict[str, List[int]]
    """
    Load PLIST
    # music_folder -> $HOME/Music/Music/Media.localized
    # tracks: (107, )
    """

    # Load Plist
    plist = plistlib.readPlist(args.plist)
    scheme = 'file://'
    music_folder = os.path.join(plist['Music Folder'][len(scheme):], 'Music/')
    tracks = {int(key): urllib.url2pathname(
        val['Location'][(len(scheme) + len(music_folder)):]) for key, val in plist['Tracks'].items()}  # type: Dict[int, str]
    playlists = {d['Name']: [t['Track ID']
                             for t in d['Playlist Items']] for d in plist['Playlists']}  # type: Dict[str, List[int]]

    return (music_folder, tracks, playlists)


def copy(args, music_folder, tracks):
    # type: (argparse.Namespace, str, Dict[int, str])

    print('Copy Items...')
    for _, f in tqdm(tracks.items()):
        src = music_folder + f
        dst = os.path.join(args.output, 'MUSIC', f)
        if not os.path.exists(src):
            print('No such file or directroy:', src)
            print(f)
            return
        if not os.path.exists(os.path.dirname(dst)):
            try:
                os.makedirs(os.path.dirname(dst))
            except OSError as e:
                print('mkdir failed:', os.path.dirname(dst))
                # print(e)
                return
        if os.path.exists(dst):
            continue
        # Copy Music File
        try:
            shutil.copy(src, dst)
            shutil.copystat(src, dst)
        except Exception as e:
            print(e)
            return

    return


def dump(args, tracks, playlists):
    # type: (argparse.Namespace, str, Dict[int, str], Dict[str, List[int]]) -> ()
    """
    Dumps Playlists
    """

    dst = os.path.join(args.output, 'MUSIC')

    print('Dump Playlists...')
    for name, lst in tqdm(playlists.items()):
        fp = os.path.join(dst, name + '.M3U8')
        with open(fp, 'w') as f:
            f.write('#EXTM3U\n')
            for tid in lst:
                if tid not in tracks:
                    continue
                f.write('#EXTINF:,\n')
                f.write(tracks[tid] + '\n')

    return


def parse():
    # type: () -> argparse.Namespace
    """
    Parse arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('plist', metavar='PLIST',
                        help='iTunes Music Library Plist')
    parser.add_argument('-o', '--output', metavar='WALKMAN',
                        default='/Volumes/WALKMAN')
    return parser.parse_args()


def main():
    # type: () -> ()
    """
    Main Function
    """

    # Parse arguments
    args = parse()

    # Load Plist
    music_folder, tracks, playlists = load(args)

    # Copy Music
    copy(args, music_folder, tracks)

    # Dump playlist
    dump(args, tracks, playlists)

    return


if __name__ == '__main__':
    main()
