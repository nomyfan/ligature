#!/usr/bin/env python
import os
import sys
import re
from glob import glob
from ligaturize import ligaturize_font
from tasks import tasks

# Rebuild script for ligaturized fonts.
# Uses ligaturize.py to do the heavy lifting; this file basically just contains
# the mapping from input font paths to output fonts.

# For the prefixed_fonts below, what word do we stick in front of the font name?
LIGATURIZED_FONT_NAME_SUFFIX = 'Ligatured'

# If copying individual characters, how different in width (relative to the font
# we're ligaturizing) should they be before we attempt to width-correct them?
# The default (0.1) means to width-correct if they're +/- 10%. Values >1.0
# effectively disable this feature.
SCALE_CHARACTER_GLYPHS_THRESHOLD = 0.1

# If copying individual characters, how different in width (relative to the font
# we're ligaturizing) should they be before we attempt to width-correct them?
# The default (0.1) means to width-correct if they're +/- 10%. Values >1.0
# effectively disable this feature.
SCALE_LIGATURE_THRESHOLD = 0.044

for task in tasks:
    input_pattern = task['input']
    input_files = glob(input_pattern)

    if not input_files:
        print("Error: pattern '%s' didn't match any files." % input_pattern)
        sys.exit(1)

    for liga_pattern in task['ligatures']:
        liga_files = glob(liga_pattern)
        if not liga_files:
            print("Error: pattern '%s' didn't match any files." % liga_pattern)
            sys.exit(1)

        for input_file in input_files:

            for liga_file in liga_files:
                liga_font_splits = re.split(r'-|\s', os.path.splitext(os.path.basename(liga_file))[0])
                liga_font_family = liga_font_splits[0]
                liga_font_style = liga_font_splits[1:]

                # grab all upper case letters of the font family
                ligatured_font_family = ''.join(list(filter(lambda x: x.isupper(), list(liga_font_family))))

                for copy_character_glyphs in [True, False]:
                    copied_character_glyphs_suffix = '-CCG' if copy_character_glyphs else ''
                    ligaturize_font(
                        input_font_file=input_file,
                        ligature_font_file=liga_file,
                        output_dir='output/',
                        output_name=None,
                        suffix="%s-%s%s" % (ligatured_font_family, LIGATURIZED_FONT_NAME_SUFFIX, copied_character_glyphs_suffix),
                        copy_character_glyphs=copy_character_glyphs,
                        scale_character_glyphs_threshold=SCALE_CHARACTER_GLYPHS_THRESHOLD,
                        scale_ligature_threshold=SCALE_LIGATURE_THRESHOLD
                    )
