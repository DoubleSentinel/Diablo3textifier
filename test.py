import re
import urllib
import os
from urllib import request


def download_icon(link, directory, sex, character):
    urllib.request.urlretrieve(link, directory + link.replace('demonhunter_male', character + '_' + sex).split('/')[-1])


def get_links(source, item, download=False):
    # for now catches only male legendary and set items												[A-Z_\:0-9a-z]*
    for link in re.findall(
            '[\bhttps://blzmedia\-a.akamaihd.net/d3/icons/items/large/\b]+[A-Z_\:0-9a-z]*[0-9]{2,50}[A-Z_\:0-9a-z]*.png',
            source):
        if download:
            directory = os.getcwd() + '\\database\\' + item + '\\'
            if not os.path.exists(directory):
                os.makedirs(directory)
            for character in characters:
                download_icon(link, directory, 'male', character)
                download_icon(link, directory, 'female', character)
        else:
            print(link.replace('demonhunter_male', 'demonhunter_female'))


if __name__ == '__main__':
    characters = ['barbarian', 'crusader', 'demonhunter', 'monk', 'wizard', 'witchdoctor']
    items = ['helm',
             'spirit-stone',
             'voodoo-mask',
             'wizard-hat',
             'pauldrons',
             'chest-armor',
             'cloak',
             'bracers',
             'gloves',
             'belt',
             'mighty-belt',
             'pants',
             'boots',
             'amulet',
             'ring',
             'shield',
             'crusader-shield',
             'mojo',
             'orb',
             'quiver',
             'axe-1h',
             'dagger',
             'mace-1h',
             'spear',
             'sword-1h',
             'ceremonial-knife',
             'fist-weapon',
             'flail-1h',
             'mighty-weapon-1h',
             'axe-2h',
             'mace-2h',
             'polearm',
             'staff',
             'sword-2h',
             'daibo',
             'flail-2h',
             'mighty-weapon-2h',
             'bow',
             'crossbow',
             'hand-crossbow',
             'wand'
             ]
    for item in items:
        for i in range(1, 6):
            try:
                get_links(urllib.request.urlopen(
                    'https://us.battle.net/d3/en/item/' + item + '/#type=legendary&page=' + str(i)).read().decode(
                    'utf-8'), item, True)
            except:
                pass
