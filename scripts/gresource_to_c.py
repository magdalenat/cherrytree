#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 'xmllint' optional to strip svg xml files (sudo apt install libxml2-utils)

import os
import subprocess
import glob
import xml.etree.ElementTree as ET
import html

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
ICONS_DIR = os.path.join(ROOT_DIR, "icons")
SRC_DIR = os.path.join(ROOT_DIR, "src", "ct")
GRESOURCE_XML_FILEPATH = os.path.join(ROOT_DIR, "icons.gresource.xml")
GRESOURCE_SOURCE_FILEPATH_NOEXT = os.path.join(SRC_DIR, "icons.gresource")

# https://developer.gnome.org/gtkmm-tutorial/stable/sec-gio-resource.html.en
#
# <?xml version="1.0" encoding="UTF-8"?>
# <gresources>
#   <gresource prefix="/icons">
#     <file preprocess="xml-stripblanks" compressed="true">filepath.svg</file>
#   </gresource>
# </gresources>

def main(args):
    # write gresource xml
    gresources_Element = ET.Element("gresources")
    gresource_Element = ET.SubElement(gresources_Element, "gresource", prefix="/icons")
    for svg_filepath in glob.glob(os.path.join(ICONS_DIR, "*.svg")):
        file_Element = ET.SubElement(gresource_Element, "file", preprocess="xml-stripblanks", compressed="true")
        file_Element.text = html.escape(os.path.basename(svg_filepath))
    gresources_ElementTree = ET.ElementTree(gresources_Element)
    gresources_ElementTree.write(GRESOURCE_XML_FILEPATH, xml_declaration=True, encoding='UTF-8')

    # convert gresource xml to source file
    shell_cmd = ("glib-compile-resources", "--target="+GRESOURCE_SOURCE_FILEPATH_NOEXT+".cc", "--generate-source", GRESOURCE_XML_FILEPATH)
    subprocess.call(shell_cmd, cwd=ICONS_DIR)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
