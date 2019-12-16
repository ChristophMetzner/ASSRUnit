################################################
# Database of experimental observations	       #
# 					       #
# The idea is to create database entries here  #
# and save everything, so that the database    #
# can be loaded whenever needed.               #
################################################


import pickle

# Each study is represented by 3 (or in the end maybe even more) different entries:
# ..._full: contains all observations from this study
# ..._full_qual: contains the same observations as ..._full, however, does not quantify differences (such as a ratio between controls and patients mean power values)
#           Instead only qualitative differences are described (so far, 3 levels [lower, equal, higher], maybe eventually 5 or more levels?) TODO: this should now be calculated from full


# Kwon et al., Arch Gen Psychiatry, 1999

kwon_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [13.8, 6.21],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.81,
            "SE": 0.37,
            "p-value": 0.03,
        },
        "3030": {
            "groups": ["control", "schiz"],
            "values": [8.63, 8.97],
            "description": "30 Hz power at 30 Hz drive",
        },
        "2020": {
            "groups": ["control", "schiz"],
            "values": [4.83, 9.66],
            "description": "20 Hz power at 20 Hz drive",
        },
        "2040": {
            "groups": ["control", "schiz"],
            "values": [1.38, 4.49],
            "description": "20 Hz power at 40 Hz drive",
        },
        "4020": {
            "groups": ["control", "schiz"],
            "values": [5.52, 3.11],
            "description": "40 Hz power at 20 Hz drive",
        },
    },
    "Meta": {
        "Measure": {
            "Value": "Mean Absolute Power",
            "Location": "Midline frontal electrode",
            "Modality": "EEG",
            "Processing": "Butterworth bandpass-filtered time averages followed by Fourier transform",
        },
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "15(Ctrl) and  15(Scz)",
            "No. Sex of HC": {"Male": 15, "Female": 0},
            "No. Sex of SZ": {"Male": 15, "Female": 0},
            "Mean Age": {"HC": 44.6, "SZ": 43.3},
            "Patient Group": "Chronic",
            "Mean illness duration": 21.1,
            "Medication Status": "Mixed",
        },
        "Paradigm": "Click-train",
        "Comments": "Values estimated from figures, since values are not provided",
    },
}

kwon_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        },
        "3030": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "30 Hz power at 30 Hz drive",
        },
        "2020": {
            "groups": "control vs. schiz",
            "value": "higher",
            "description": "20 Hz power at 20 Hz drive",
        },
        "2040": {
            "groups": "control vs. schiz",
            "value": "higher",
            "description": "20 Hz power at 40 Hz drive",
        },
        "4020": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 20 Hz drive",
        },
    },
    "Meta": {
        "Measure": {
            "Value": "Mean Absolute Power",
            "Location": "Midline frontal electrode",
            "Modality": "EEG",
            "Processing": "Butterworth bandpass-filtered time averages followed by Fourier transform",
        },
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "15(Ctrl) and  15(Scz)",
            "No. Sex of HC": {"Male": 15, "Female": 0},
            "No. Sex of SZ": {"Male": 15, "Female": 0},
            "Mean Age": {"HC": 44.6, "SZ": 43.3},
            "Patient Group": "Chronic",
            "Mean illness duration": 21.1,
            "Medication Status": "Mixed",
        },
        "Paradigm": "Click-train",
        "Comments": "Values estimated from figures, since values are not provided",
    },
}

kwon = {"Full": kwon_full, "Full_qual": kwon_full_qual}

# Vierling-Claassen et al.,Neurophysiol, 2008

vierling_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [1.2 * 10e-19, 0.42 * 10e-19],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -1.50,
            "SE": 0.45,
            "p-value": "<0.01",
        },
        "3030": {
            "groups": ["control", "schiz"],
            "values": [0.75 * 10e-19, 0.99 * 10e-19],
            "description": "30 Hz power at 30 Hz drive",
        },
        "2020": {
            "groups": ["control", "schiz"],
            "values": [0.36 * 10e-19, 0.78 * 10e-19],
            "description": "20 Hz power at 20 Hz drive",
        },
        "2040": {
            "groups": ["control", "schiz"],
            "values": [0.21 * 10e-19, 0.51 * 10e-19],
            "description": "20 Hz power at 40 Hz drive",
        },
        "4020": {
            "groups": ["control", "schiz"],
            "values": [0.51 * 10e-19, 0.18 * 10e-19],
            "description": "40 Hz power at 20 Hz drive",
        },
    },
    "Meta": {
        "Measure": {
            "Value": "Mean Absolute Power",
            "Location": "Left hemisphere",
            "Modality": "MEG",
            "Processing": "Time-averaging followed by PSD using Welch`s method",
        },
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "12(Ctrl) and  12(Scz)",
            "No. Sex of HC": {"Male": 12, "Female": 0},
            "No. Sex of SZ": {"Male": 18, "Female": 0},
            "Mean Age": {"HC": "", "SZ": ""},
            "Patient Group": "Chronic",
            "Mean illness duration": 26.2,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "Click-train",
        "Comments": "Values estimated from figures, since values are not provided",
    },
}

vierling_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        },
        "3030": {
            "groups": "control vs. schiz™",
            "value": "equal",
            "description": "30 Hz power at 30 Hz drive",
        },
        "2020": {
            "groups": "control vs. schiz",
            "value": "higher",
            "description": "20 Hz power at 20 Hz drive",
        },
        "2040": {
            "groups": "control vs. schiz",
            "value": "higher",
            "description": "20 Hz power at 40 Hz drive",
        },
        "4020": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 20 Hz drive",
        },
    },
    "Meta": {
        "Measure": {
            "Value": "Mean Absolute Power",
            "Location": "Left hemisphere",
            "Modality": "MEG",
            "Processing": "Time-averaging followed by PSD using Welch`s method",
        },
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "12(Ctrl) and  12(Scz)",
            "No. Sex of HC": {"Male": 12, "Female": 0},
            "No. Sex of SZ": {"Male": 18, "Female": 0},
            "Mean Age": {"HC": "", "SZ": ""},
            "Patient Group": "Chronic",
            "Mean illness duration": 26.2,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "Click-train",
        "Comments": "Values estimated from figures, since values are not provided",
    },
}

vierling = {"Full": vierling_full, "Full_qual": vierling_full_qual}

# Krishnan et al., Neuroimage, 2009


krishnan_full = {
    "Data": {
        "0505": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "5 Hz power at 5 Hz drive",
            "hedges-g": -0.66,
            "SE": 0.31,
            "p-value": 0.04,
        },
        "1010": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "10 Hz power at 10 Hz drive",
        },
        "1515": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "15 Hz power at 15 Hz drive",
        },
        "2020": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "20 Hz power at 20 Hz drive",
        },
        "2525": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "25 Hz power at 25 Hz drive",
        },
        "3030": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "30 Hz power at 30 Hz drive",
        },
        "3535": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "35 Hz power at 35 Hz drive",
        },
        "4040": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "40 Hz power at 40 Hz drive",
        },
        "4545": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "45 Hz power at 45 Hz drive",
        },
        "5050": {
            "groups": ["control", "schiz"],
            "values": [1.0, 1.0],
            "description": "50 Hz power at 50 Hz drive",
        },
    },
    "Meta": {
        "Measure": {
            "Value": "Mean baseline corrected power",
            "Electrode/Position": "?",
        },
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "21(Ctrl) and  21(Scz)",
            "No. Sex of HC": {"Male": 11, "Female": 10},
            "No. Sex of SZ": {"Male": 13, "Female": 8},
            "Mean Age": {"HC": 40, "SZ": 42.6},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "Amplitude-modulated tones",
    },
}

krishnan_full_qual = {
    "Data": {
        "0505": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "5 Hz power at 5 Hz drive",
        },
        "1010": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "10 Hz power at 10 Hz drive",
        },
        "1515": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "15 Hz power at 15 Hz drive",
        },
        "2020": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "20 Hz power at 20 Hz drive",
        },
        "2525": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "25 Hz power at 25 Hz drive",
        },
        "3030": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "30 Hz power at 30 Hz drive",
        },
        "3535": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "35 Hz power at 35 Hz drive",
        },
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        },
        "4545": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "45 Hz power at 45 Hz drive",
        },
        "5050": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "50 Hz power at 50 Hz drive",
        },
        "2040": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "20 Hz power at 40 Hz drive",
        },
        "4020": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "40 Hz power at 20 Hz drive",
        },
    },
    "Meta": {
        "Measure": {
            "Value": "Mean baseline corrected power",
            "Location": "Cz in a 10-20 setting",
            "Modality": "EEG",
            "Processing": "Least square linear FIR filtered and Hilbert transformed",
        },
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "21(Ctrl) and  21(Scz)",
            "No. Sex of HC": {"Male": 11, "Female": 10},
            "No. Sex of SZ": {"Male": 13, "Female": 8},
            "Mean Age": {"HC": 40, "SZ": 42.6},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "Amplitude-modulated tones; carrier freqeuncy 1kHz",
    },
}

krishnan = {"Full": krishnan_full, "Full_qual": krishnan_full_qual}


# Hamm et al.,Schizophr Res,2012
hamm_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": 0.53,
            "SE": 0.35,
            "p-value": 0.13,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "16(Ctrl) and  17(Scz)",
            "No. Sex of HC": {"Male": 9, "Female": 7},
            "No. Sex of SZ": {"Male": 11, "Female": 6},
            "Mean Age": {"HC": 39.5, "SZ": 41.5},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

hamm_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "16(Ctrl) and  17(Scz)",
            "No. Sex of HC": {"Male": 9, "Female": 7},
            "No. Sex of SZ": {"Male": 11, "Female": 6},
            "Mean Age": {"HC": 39.5, "SZ": 41.5},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}
hamm = {"Full": hamm_full, "Full_qual": hamm_full_qual}

# Hong et al.,Schizophr Res ,2004
hong_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": 0.20,
            "SE": 0.31,
            "p-value": 0.53,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "17(Ctrl) and  24(Scz)",
            "No. Sex of HC": {"Male": 8, "Female": 9},
            "No. Sex of SZ": {"Male": 14, "Female": 10},
            "Mean Age": {"HC": 41.1, "SZ": 39.7},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

hong_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "17(Ctrl) and  24(Scz)",
            "No. Sex of HC": {"Male": 8, "Female": 9},
            "No. Sex of SZ": {"Male": 14, "Female": 10},
            "Mean Age": {"HC": 41.1, "SZ": 39.7},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

hong = {"Full": hong_full, "Full_qual": hong_full_qual}

# Hirano et al.,JAMA Psychiatry,2015
hirano_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.09,
            "SE": 0.28,
            "p-value": 0.76,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "24(Ctrl) and  24(Scz)",
            "No. Sex of HC": {"Male": 20, "Female": 4},
            "No. Sex of SZ": {"Male": 20, "Female": 4},
            "Mean Age": {"HC": 44.1, "SZ": 46},
            "Patient Group": "Chronic",
            "Mean illness duration": 21.1,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

hirano_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "24(Ctrl) and  24(Scz)",
            "No. Sex of HC": {"Male": 20, "Female": 4},
            "No. Sex of SZ": {"Male": 20, "Female": 4},
            "Mean Age": {"HC": 44.1, "SZ": 46},
            "Patient Group": "Chronic",
            "Mean illness duration": 21.1,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

hirano = {"Full": hirano_full, "Full_qual": hirano_full_qual}

# Rass et al,Schizophr Res,2012
rass_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.35,
            "SE": 0.20,
            "p-value": 0.09,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "56(Ctrl) and 42 (Scz)",
            "No. Sex of HC": {"Male": 26, "Female": 30},
            "No. Sex of SZ": {"Male": 23, "Female": 19},
            "Mean Age": {"HC": 38.75, "SZ": 36.86},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

rass_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "56(Ctrl) and 42 (Scz)",
            "No. Sex of HC": {"Male": 26, "Female": 30},
            "No. Sex of SZ": {"Male": 23, "Female": 19},
            "Mean Age": {"HC": 38.75, "SZ": 36.86},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

rass = {"Full": rass_full, "Full_qual": rass_full_qual}

# Spencer et al.,Biol Psychiatry,2008
spencer_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.55,
            "SE": 0.31,
            "p-value": 0.07,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "33(Ctrl) and  16(Scz)",
            "No. Sex of HC": {"Male": 19, "Female": 14},
            "No. Sex of SZ": {"Male": 19, "Female": 14},
            "Mean Age": {"HC": 27.5, "SZ": 25.5},
            "Patient Group": "FEP",
            "Mean illness duration": 13.6,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

spencer_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "equal",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "33(Ctrl) and  16(Scz)",
            "No. Sex of HC": {"Male": 19, "Female": 14},
            "No. Sex of SZ": {"Male": 19, "Female": 14},
            "Mean Age": {"HC": 27.5, "SZ": 25.5},
            "Patient Group": "FEP",
            "Mean illness duration": 13.6,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

spencer = {"Full": spencer_full, "Full_qual": spencer_full_qual}

# Brenner et al.,Am J Psychiatry,2003
brenner_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.67,
            "SE": 0.31,
            "p-value": 0.03,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "22(Ctrl) and  21(Scz)",
            "No. Sex of HC": {"Male": 13, "Female": 9},
            "No. Sex of SZ": {"Male": 18, "Female": 3},
            "Mean Age": {"HC": 39.7, "SZ": 45.6},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

brenner_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "22(Ctrl) and  21(Scz)",
            "No. Sex of HC": {"Male": 13, "Female": 9},
            "No. Sex of SZ": {"Male": 18, "Female": 3},
            "Mean Age": {"HC": 39.7, "SZ": 45.6},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

brenner = {"Full": brenner_full, "Full_qual": brenner_full_qual}

# Tsuchimoto et al.,Schizophr Res. ,2011
tsuchimoto_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.77,
            "SE": 0.33,
            "p-value": 0.02,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "22(Ctrl) and 17 (Scz)",
            "No. Sex of HC": {"Male": 9, "Female": 13},
            "No. Sex of SZ": {"Male": 6, "Female": 11},
            "Mean Age": {"HC": 37, "SZ": 35.6},
            "Patient Group": "Chronic",
            "Mean illness duration": 13.5,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

tsuchimoto_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "22(Ctrl) and 17 (Scz)",
            "No. Sex of HC": {"Male": 9, "Female": 13},
            "No. Sex of SZ": {"Male": 6, "Female": 11},
            "Mean Age": {"HC": 37, "SZ": 35.6},
            "Patient Group": "Chronic",
            "Mean illness duration": 13.5,
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

tsuchimoto = {"Full": tsuchimoto_full, "Full_qual": tsuchimoto_full_qual}

# Koemek et al.,Eur J Neurosci,2012
koemek_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.82,
            "SE": 0.41,
            "p-value": 0.05,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "12 (Ctrl) and 12 (Scz)",
            "No. Sex of HC": {"Male": 9, "Female": 7},
            "No. Sex of SZ": {"Male": 11, "Female": 6},
            "Mean Age": {"HC": 39.5, "SZ": 41.5},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

koemek_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "12 (Ctrl) and 12 (Scz)",
            "No. Sex of HC": {"Male": 9, "Female": 7},
            "No. Sex of SZ": {"Male": 11, "Female": 6},
            "Mean Age": {"HC": 39.5, "SZ": 41.5},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

koemek = {"Full": koemek_full, "Full_qual": koemek_full_qual}


# Hamm et al., Schizophr Res,2015
hamm2_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.89,
            "SE": 0.34,
            "p-value": 0.01,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "18 (Ctrl) and  18(Scz)",
            "No. Sex of HC": {"Male": 11, "Female": 7},
            "No. Sex of SZ": {"Male": 9, "Female": 9},
            "Mean Age": {"HC": 40.8, "SZ": 45.6},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

hamm2_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": " "},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "18 (Ctrl) and  18(Scz)",
            "No. Sex of HC": {"Male": 11, "Female": 7},
            "No. Sex of SZ": {"Male": 9, "Female": 9},
            "Mean Age": {"HC": 40.8, "SZ": 45.6},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

hamm2 = {"Full": hamm2_full, "Full_qual": hamm2_full_qual}

# Tada et al., Cereb Cortex,2016
tada_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.90,
            "SE": 0.35,
            "p-value": 0.01,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "21 (Ctrl) and  15(Scz)",
            "No. Sex of HC": {"Male": 11, "Female": 10},
            "No. Sex of SZ": {"Male": 8, "Female": 5},
            "Mean Age": {"HC": 22.4, "SZ": 22.1},
            "Patient Group": "FEP",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

tada_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "21 (Ctrl) and  15(Scz)",
            "No. Sex of HC": {"Male": 11, "Female": 10},
            "No. Sex of SZ": {"Male": 8, "Female": 5},
            "Mean Age": {"HC": 22.4, "SZ": 22.1},
            "Patient Group": "FEP",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

tada = {"Full": tada_full, "Full_qual": tada_full_qual}

# Spencer et al.,BMC Neurosci.,2009
spencer2_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -0.92,
            "SE": 0.35,
            "p-value": 0.01,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "160(Ctrl) and  18(Scz)",
            "No. Sex of HC": {"Male": 160, "Female": 0},
            "No. Sex of SZ": {"Male": 18, "Female": 0},
            "Mean Age": {"HC": 44.4, "SZ": 39.8},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

spencer2_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "160(Ctrl) and  18(Scz)",
            "No. Sex of HC": {"Male": 160, "Female": 0},
            "No. Sex of SZ": {"Male": 18, "Female": 0},
            "Mean Age": {"HC": 44.4, "SZ": 39.8},
            "Patient Group": "Chronic",
            "Mean illness duration": "",
            "Medication Status": "All Medicated",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

spencer2 = {"Full": spencer2_full, "Full_qual": spencer2_full_qual}

# Wilson et al.,Cereb Cortex.,2008
wilson_full = {
    "Data": {
        "4040": {
            "groups": ["control", "schiz"],
            "values": [],
            "description": "40 Hz power at 40 Hz drive",
            "hedges-g": -1.23,
            "SE": 0.47,
            "p-value": 0.01,
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "10 (Ctrl) and  10 (Scz)",
            "No. Sex of HC": {"Male": 4, "Female": 6},
            "No. Sex of SZ": {"Male": 7, "Female": 3},
            "Mean Age": {"HC": 15.82, "SZ": 14.64},
            "Patient Group": "Early Onset",
            "Mean illness duration": 3.4,
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

wilson_full_qual = {
    "Data": {
        "4040": {
            "groups": "control vs. schiz",
            "value": "lower",
            "description": "40 Hz power at 40 Hz drive",
        }
    },
    "Meta": {
        "Measure": {"Value": "", "Location": "", "Modality": "", "Processing": ""},
        "Subjects": {
            "Group": "Schizophrenia vs Control",
            "Number of subjects": "10 (Ctrl) and  10 (Scz)",
            "No. Sex of HC": {"Male": 4, "Female": 6},
            "No. Sex of SZ": {"Male": 7, "Female": 3},
            "Mean Age": {"HC": 15.82, "SZ": 14.64},
            "Patient Group": "Early Onset",
            "Mean illness duration": 3.4,
            "Medication Status": "Mixed",
        },
        "Paradigm": "",
        "Comments": "",
    },
}

wilson = {"Full": wilson_full, "Full_qual": wilson_full_qual}

# Combine all dictionaries
database = {
    "Kwon_1999": kwon,
    "Vierling_2008": vierling,
    "Krishnan_2009": krishnan,
    "Hamm_2012": hamm,
    "Hong_2004": hong,
    "Hirano_2015": hirano,
    "Rass_2012": rass,
    "Spencer_2008": spencer,
    "Brenner_2003": brenner,
    "Tsuchimoto_2011": tsuchimoto,
    "Koemek_2012": koemek,
    "Hamm_2015": hamm2,
    "Tada_2016": tada,
    "Spencer_2009": spencer2,
    "Wilson_2008": wilson,
}


def saveObj(obj, name):
    with open(name + ".pkl", "wb") as f:
        pickle.dump(obj, f, protocol=2)


saveObj(database, "Databases/ASSR_schizophrenia_experimental_database")
