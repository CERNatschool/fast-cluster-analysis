#!/usr/bin/env python

"""
Error messages that might be raised when creating datasets.
"""

DATA_ERROR_MESSAGES = {
    "NOT_EXIST"    : "\
<p>The folder you have selected does not exist.</p> \
<p>Please select a folder that <strong>exists</strong> and, preferably, \
contains some valid data files.</p> \
",
    "FOLDER_EMPTY" : "\
<p>The folder that you have selected is empty.</p> \
<p>Please select the folder that contains your data files.</p> \
",
    "BAD_FORMAT" : "\
<p>The folder contains a file in an unrecognised format.</p> \
",
    "CONTAINS_DIR" : "\
<p>The folder that you have selected contains another folder.</p> \
<p>Directories containing data to be analysed should not contain \
other folders. Please check that you have selected the correct \
folder and that your data is arranged as it should be.</p> \
",
    "FORMAT_MISMATCH" : "\
<p>Data files have been found in two or more valid formats.</p> \
<p>This suggests that the data in the selected folder has been \
collected in one or more separate runs with differing detector \
settings. Please check your data and the detector configurations \
used.</p> \
",
    "MISSING_DSC" : "\
<p>One or more of the data files in the selected folder is missing \
a DSC (detector settings) file.</p> \
",
    "MISSING_DAT" : "\
<p>One or more of the DSC files in the selected folder is missing \
a data file.</p> \
",
    "DET_DIFF_CHIPIDS" : "\
<p>The Pixelman dataset supplied contains data from different \
detectors.</p> \
",
    "DET_DIFF_NANDSN" : "\
<p>The Pixelman dataset supplied contains data from different \
detectors.</p> \
",
    "PIXEL_MASK_IN_DB" : "\
<p>A pixel mask with that name is already in the database.</p>\
",
    "NO_SOURCE_NAME" : "\
<p>There is currently no source name specified.</p> \
<p>Please select a source from the database or enter a new name \
in the <strong>Source Name</strong> field.</p>\
",
    "NO_SOURCE_DESC" : "\
<p>There is currently no source description specified.</p> \
<p>Please enter a description of the source for the dataset to \
import, or select a source from the database.</p> \
",
    "FRAME_NO_HV" : "\
<p>You are trying to create a frame but no bias voltage (HV) \
value has been supplied.</p>
",
    "FRAME_NO_IKRUM" : "\
<p>You are trying to create a frame but no I_Krum value
has been supplied.</p>
"
    }
