import re
import urllib
import os
from urllib import request
import sys
from bs4 import BeautifulSoup


def download_item_icon(link, directory, sex, character, name=''):
    if name == '':
        filename = character + '_' + sex + '.png'
    else:
        filename = name + '_' + character + '_' + sex + '.png'
    print('checking: ' + filename)
    if os.path.isfile(directory + filename):
        print('\tfile exists, skipping')
        return
    try:
        print('downloading...')
        if character == 'crusader':
            try:
                urllib.request.urlretrieve(link.replace('demonhunter_male', 'x1_' + character + '_' + sex),
                                       directory + filename)
                return
            except urllib.error.URLError:
                urllib.request.urlretrieve(link.replace('demonhunter_male', character + '_' + sex),
                                           directory + filename)
        else:
            urllib.request.urlretrieve(link.replace('demonhunter_male', character + '_' + sex), directory + filename)
        print('\t'+filename + ' downloaded!\n')
    except urllib.error.URLError:
        print('\tremote file doesn\'t exist, skipping\n')
        pass
    except KeyboardInterrupt:
        exit(0)
    except:
        print('\tdownload failed, skipping\n')
        pass


def download_spell_icon(link, directory):
    filename = link.split('/')[-1]
    if 'male' not in filename:
        if os.path.isfile(directory + filename):
            print('\tfile exists, skipping\n')
            return
        try:
            print('downloading...')
            print(link)
            urllib.request.urlretrieve(link, directory + filename)
            print('\t' + filename + ' downloaded!\n')
        except urllib.error.URLError:
            print('\tremote file doesn\'t exist, skipping\n')


def get_item_links(source, item, rarity, download=False):
    soup = BeautifulSoup(source, 'html.parser')
    for tr in soup.find_all('tr', rarity):
        link = re.findall('url\((.*?)\)', str(tr.find_all('span', style=re.compile("background-image: "))[0]))[0]
        name = tr.find_all('a')[1].string
        if download:
            directory = os.getcwd() + '\\database\\items\\' + item + '\\'
            if not os.path.exists(directory):
                os.makedirs(directory)
            for character in characters:
                download_item_icon(link, directory, 'male', character, name)
                download_item_icon(link, directory, 'female', character, name)
        else:
            print('name: '+name)
            print('\tlink: '+link)


def get_class_links(source, character, download=False):
    for link in re.findall('[\bhttps://blzmedia\-a.akamaihd.net/d3/icons/skills/64/\b]+[a-z_0-9]*_[a-z]*.png', source):
        if download:
            dir = os.getcwd() + '\\database\\spells\\' + character + '\\'
            if not os.path.exists(dir):
                os.makedirs(dir)
            download_spell_icon(link, dir)
        else:
            print(link)


if __name__ == '__main__':
    args = sys.argv
    characters = ['barbarian', 'crusader', 'demonhunter', 'monk', 'wizard', 'witchdoctor']
    items = ['helm', 'spirit-stone', 'voodoo-mask', 'wizard-hat', 'pauldrons', 'chest-armor', 'cloak', 'bracers',
             'gloves', 'belt', 'mighty-belt', 'pants', 'boots', 'amulet',
             'ring', 'shield', 'crusader-shield', 'mojo', 'orb', 'quiver', 'axe-1h', 'dagger', 'mace-1h', 'spear',
             'sword-1h', 'ceremonial-knife', 'fist-weapon', 'flail-1h',
             'mighty-weapon-1h', 'axe-2h', 'mace-2h', 'polearm', 'staff', 'sword-2h', 'daibo', 'flail-2h',
             'mighty-weapon-2h', 'bow', 'crossbow', 'hand-crossbow', 'wand']
    if 'items' in args:
        if len(args) == 2:
            print("Please give one of the following rarities: common, legendary")
            print(
                "However, for common items, we don't guarantee the image treatment algorithm will differentiate items with the same icon")
        else:
            if "common" in args:
                for item in items:
                    get_item_links(urllib.request.urlopen(
                        'https://us.battle.net/d3/en/item/' + item + '/').read().decode('utf-8'), item, "common",
                                   True)
                print('\nItems icons download finished!')
            elif "legendary" in args:
                for item in items:
                    get_item_links(urllib.request.urlopen(
                        'https://us.battle.net/d3/en/item/' + item + '/').read().decode('utf-8'), item, "legendary",
                                   True)
                    get_item_links(urllib.request.urlopen(
                        'https://us.battle.net/d3/en/item/' + item + '/').read().decode('utf-8'), item, "set",
                                   True)
                print('\nItems icons download finished!')
    if 'chars' in args:
        for char in characters:
            dir = os.getcwd() + '\\database\\characters\\'
            if not os.path.exists(dir):
                os.makedirs(dir)
            download_item_icon('https://blzmedia-a.akamaihd.net/d3/icons/portraits/42/demonhunter_male.png',
                               dir, 'male', char)
            download_item_icon('https://blzmedia-a.akamaihd.net/d3/icons/portraits/42/demonhunter_male.png',
                               dir, 'female', char)
        print('\nCharacter icons download finished!')
    if 'spells' in args:
        for char in characters:
            if char == 'demonhunter':
                char = 'demon-hunter'
            if char == 'witchdoctor':
                char = 'witch-doctor'
            get_class_links(urllib.request.urlopen(
                'https://us.battle.net/d3/en/class/' + char + '/active/').read().decode('utf-8'), char, True)
            get_class_links(urllib.request.urlopen(
                'https://us.battle.net/d3/en/class/' + char + '/passive/').read().decode('utf-8'), char, True)
        print('\nSpells icons download finished!')
    if len(args) == 1:
        print('Please insert one of the following arguments: spells, items, or chars')
