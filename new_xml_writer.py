#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a script to convert the 'old' form of the Archimob xml
into the new 'Heath approved form'

Some things that are going to be in here that won't be filled out:

-there will be a 'time' element, but it won't be entered
-For the sake of this example, 'sentances' will be just defined
    by the '/', rather than by turns
"""

from lxml import etree

final_word_list = []

tree = etree.parse("archimob_test.xml")
root = tree.getroot()


for child in root:
    # this goes through 'document'
    for child1 in child:
        # this is each turn
        # print child1.tag, child1.attrib
        
        # I'm grabbing the speaker and the id
        # to give the later elements an id
        speaker_id = child1.get('speaker')
        turn_id = child1.get('id')

        for child2 in child1:
            # print child2.text
            # print child2.get('de_form')
            
            # append tuple of id, swiss word and then normalized word
            # to the 'final list'
            final_word_list.append((speaker_id, child2.text, child2.get('de_form')))


"""
Okay, now we're going to write the new xml structure
"""

# root element
root = etree.Element('dialogue')

# elements, defining
sentence = etree.SubElement(root,'u')
sentence.set('id', final_word_list[0][0])
sentence.set('uID', 'u0')

# this is a variable, used to do id's for the u elements
u_count = 1

# go through final_word_list, write it to the thing
for ch_tuple in final_word_list:
    # Make a new sentence if there's a /
    if ch_tuple[2] == '/':
        # so before a new <u> is created, we finish the previous one with
        # a media tag
        media_tag = etree.SubElement(sentence, 'media')
        media_tag.set('start', '0')
        media_tag.set('end', '0')

        # create a new <u>
        sentence = etree.SubElement(root, 'u')

        # add the tags
        sentence.set('id', ch_tuple[0])

        # okay, so I'm making the id here, just tacking a u in front of the count
        sentence.set('uID', 'u' + str(u_count))

        u_count += 1
    else:
        word = etree.SubElement(sentence, 'w')
        word.text = ch_tuple[1]
        # add the 'normalized form'
        word.set('normalized', ch_tuple[2])
        word.set('POS', 'UNK')


# write it
tree = etree.ElementTree(root)
tree.write('test.xml', xml_declaration=True, encoding='utf-8')
