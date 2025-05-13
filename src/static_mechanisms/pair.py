from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class Pair:
    """
    Represents a patient-donor pair in the liver-exchange mechanism.

    Attributes:
        id: Unique identifier for the pair.
        X: Patient's size & blood-type vector (size1, size2, blood_code).
        Yl: Donor's left-lobe thresholds (max patient vector donor's left lobe can serve).
        Yr: Donor's right-lobe thresholds (max patient vector donor's right lobe can serve).
        willing: True if the donor is willing to donate the right lobe (w_i = w), else False (u).
        direct: True if the pair prefers a direct deceased-donor transplant over any exchange of the same lobe (d_i = d), else False (m).
    """
    id: int
    X: Tuple[float, float, float]
    Yl: Tuple[float, float, float]
    Yr: Tuple[float, float, float]
    willing: bool
    direct: bool


def transplant_type(donor: Pair, patient: Pair) -> Optional[str]:
    """
    Determine which lobe (if any) donor j can give to patient i.

    Implements Definition 1 from Ergin et al (2020):
    Returns:
        'l'  donors left lobe is feasible,
        'r'   only donors right lobe is feasible,
        None  donor cannot transplant to this patient.
    """
    # Check left‐lobe feasibility
    if all(px <= yl for px, yl in zip(patient.X, donor.Yl)):
        return 'l'

    # Check right‐lobe feasibility
    if all(px <= yr for px, yr in zip(patient.X, donor.Yr)):
        return 'r'

    # Neither lobe can accommodate the patient
    return None
