#!/usr/bin/env python

"""
Convenience values for dataset processing.
"""

DATA_FILE_TYPES = {
    0    : "Unknown",
    18   : "ASCII Matrix",
    8210 : "ASCII [X, C]",
    4114 : "ASCII [x, y, C]",
    17   : "Binary Matrix",
    8209 : "Binary [X, C]",
    4113 : "Binary [x, y, C]",
    #
    -1   : "DSC",
    -2   : "Empty"
    }

ACQ_MODES = {
    1 : "Started immediately, Stopped by timer",
    2 : "Started immediately, Stopped by SW trigger",
    3 : "Started by SW trigger, Stopped by timer",
    4 : "Started by SW trigger, Stopped by SW trigger"
    }

ACQ_TIME_UNITS_SHORT = "s"

ACQ_TIME_UNITS = "seconds"

HW_TIME_MODES = {
    1 : "Hardware",
    2 : "PC",
    3 : "Automatic"
    }

MPX_TYPES = {
    1 : "2.1",
    2 : "MXR",
    3 : "TPX"
    }

MPX_TYPES_LONG = {
    1 : "Medipix 2.1",
    2 : "Medipix MXR",
    3 : "Timepix"
    }

POLARITIES = {
    0 : "Negative (electrons)",
    1 : "Posiive (holes)"
    }

TPX_CLOCK_VALS = {
    0 : 10.0,
    1 : 20.0,
    2 : 40.0,
    3 : 80.0
    }


# Column headings

ID_HEADER = "ID"

FRAME_WIDTH_HEADER = "Width"

FRAME_HEIGHT_HEADER = "Height"

FRAME_FORMAT_HEADER = "Format"

PIXELS_HEADER = "Pixels"

N_PIXELS_HEADER = "No. of Pixels"

N_UNMASKED_PIXELS_HEADER = "No. of Unmasked Pixels"

N_MASKED_PIXELS_HEADER = "No. of Masked Pixels"

OCCUPANCY_HEADER = "Occupancy"

OCCUPANCY_PC_HEADER = "Occupancy (\%)"

PIXEL_MASK_HEADER = "Pixel Mask"

DETECTOR_HEADER = "Detector"

DET_SETTINGS_HEADER = "Detector Settings"

START_TIME_HEADER = "Start Time"

START_TIME_SUB_SEC_HEADER = "Start Time (Sub-second)"

END_TIME_HEADER = "End Time"

END_TIME_SUB_SEC_HEADER = "End Time (Sub-second)"

ACQ_TIME_HEADER = "Acq. Time"

AC_TIME_UNITS = "seconds"

ACQ_TIME_UNITS_SHORT = "s"

LATITUDE_HEADER = "Latitude"

LONGITUDE_HEADER = "Longitude"

ALTITUDE_HEADER = "Altitude"

OMEGA_X_HEADER = "Omega x"

OMEGA_Y_HEADER = "Omega y"

OMEGA_Z_HEADER = "Omega z"

ROLL_HEADER = "Roll"

PITCH_HEADER = "Pitch"

YAW_HEADER = "Yaw"

SOURCE_HEADER = "Source"

RUN_HEADER = "Run"

IS_MC_HEADER = "Is MC?"

N_KLUSTERS_HEADER = "Number of Clusters"

N_GAMMAS_HEADER = "Number of Gamma Candidates"

N_G1_HEADER = "Number of Monopixel Gamma Candidates"

N_G2_HEADER = "Number of Bipixel Gamma Candidates"

N_G3_HEADER = "Number of Tripixel Gamma Candidates"

N_G4_HEADER = "Number of Tetrapixel Gamma Candidates"


# Clusters
#----------

KLUSTER_PIXELS_HEADER = "Pixels"

KLUSTER_SIZE_HEADER = "Size"

X_MIN_HEADER = "Min. x"
#
X_MAX_HEADER = "Max. x"

Y_MIN_HEADER = "Min. y"

Y_MAX_HEADER = "Max. y"

KLUSTER_WIDTH_HEADER = "Width"

KLUSTER_HEIGHT_HEADER = "Height"

KLUSTER_X_UW_HEADER = "x (UW)"

KLUSTER_Y_UW_HEADER = "y (UW)"

KLUSTER_RADIUS_UW_HEADER = "Radius (UW)"

KLUSTER_DENSITY_UW_HEADER = "Density (UW)"

KLUSTER_TOTAL_COUNTS_HEADER = "Total Counts"

KLUSTER_MAX_COUNT_HEADER = "Max. Count"

KLUSTER_LIN_M_HEADER = "m"

KLUSTER_LIN_C_HEADER = "c"

KLUSTER_LIN_SUMOFR_HEADER = "Sum(R)"

KLUSTER_LINEARITY_HEADER = "Linearity"

KLUSTER_N_EDGE_HEADER = "Number of Edge Pixels"

KLUSTER_INNERFRAC_HEADER = "Inner Pixel Fraction"

KLUSTER_OUTERFRAC_HEADER = "Outer Pixel Fraction"

KLUSTER_TOTAL_ENERGY_HEADER = "Total E"

KLUSTER_MAX_ENERGY_HEADER = "Max. E"

IS_EDGE_KLUSTER_HEADER = "Edge Cluster?"

FRAME_ID_HEADER = "Frame ID"

TRIPIXEL_RADIUS = 0.75

TETRAPIXEL_RADIUS = 0.71


# Detectors
#-----------

DET_CHIPID_HEADER = "Chip ID"

DET_CUSTOM_NAME_HEADER = "Custom Name"

DET_NAME_AND_SN_HEADER = "Name and S/N"

DET_TYPE_HEADER = "Type"

DET_FWV_HEADER = "Firmware Version"

DET_INTERFACE_HEADER = "Interface"

PIXELMANV_HEADER = "Pixelman Version"

DET_X_HEADER = "Det. x"

DET_Y_HEADER = "Det. y"

DET_Z_HEADER = "Det. z"

DET_EULERA_HEADER = "Det. Euler a"

DET_EULERB_HEADER = "Det. Euler b"

DET_EULERC_HEADER = "Det. Euler c"


# Detector Settings
#-------------------

DETSET_NAME = "Name"

DETSET_HV_HEADER = "Bias Voltage"

DETSET_IKRUM_HEADER = "I_Krum"

DETSET_DISC_HEADER = "Disc"

DETSET_PREAMP_HEADER = "Preamp"

DETSET_BUFFA_HEADER = "BuffAnalogA"

DETSET_BUFFB_HEADER = "BuffAnalogB"

DETSET_HIST_HEADER = "Hist"

DETSET_THL_HEADER = "THL"

DETSET_THLCOARSE_HEADER = "THLCoarse"

DETSET_VCAS_HEADER = "Vcas"

DETSET_FBK_HEADER = "FBK"

DETSET_GND_HEADER = "GND"

DETSET_THS_HEADER = "THS"

DETSET_BIASLVDS_HEADER = "BiasLVDS"

DETSET_REFLVDS_HEADER = "RefLVDS"

DETSET_POL_HEADER = "Polarity"

DETSET_BSP_HEADER = "BS Preamp Enabled?"

DETSET_MPXCLOCK_HEADER = "Medipix Clock"

DETSET_TPXCLOCK_HEADER = "Timepix Clock"


# Pixel Masks
#-------------

MASK_PIXELS_HEADER = "Pixels"

MASK_FORMAT_HEADER = "Format"

MASK_NAME_HEADER = "Name"

MASK_N_MASKED_HEADER = "Number of Masked Pixels"


# Runs
#------

RUN_NAME_HEADER = "Run ID"

ACQ_MODE_HEADER = "Acq. Mode"

HW_TIMER_MODE_HEADER = "HW Timer Mode"

RUN_N_FRAMES_HEADER = "Number of Frames"

DETECTOR_HEADER = "Detector"

DETSETTINGS_HEADER = "Detector Settings"

RUN_DURATION_HEADER = "Duration"


# Sources
#---------

SOURCE_NAME_HEADER = "Name"

SOURCE_DESC_HEADER = "Description"
