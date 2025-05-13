from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class Pair:
    """
    Represents a patient-donor pair in the liver-exchange mechanism.

    Attributes:
        id: Unique identifier for the pair.
        X: Patient's size & blood-type vector (size1, size2, blood type).
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
if __name__ == "__main__":
    # ——————————————————————————————————————————————————————————————————————
    #  Examples drawn from T = BxS with B={0,1}^2 (blood‐type bits) and S={0,1}
    #  Coordinate‐wise partial order “≥” on (b1,b2,s) is exactly
    #     graft X compatible with patient X'  iff  X ≥ X'  
    #  Left‐lobe only when X ≤ Y^ℓ; if that fails but X ≤ Y^r, right‐lobe only 
    # ——————————————————————————————————————————————————————————————————————

    # 1) Universal O donor (b=(1,1)): both lobes big enough 
    donor1  = Pair(
        id=1,
        X   =(1,1,0),      # donor.X unused by transplant_type, set = Yl for clarity
        Yl  =(1,1,0),      # left‐lobe: (1,1,blood‐type O), size=0
        Yr  =(1,1,1),      # right‐lobe: same bits, size=1
        willing=True,
        direct=False
    )
    patient1 = Pair(
        id=10,
        X   =(0,1,1),      # A‐type patient (0,1), size=1
        Yl  =(0,1,1),      # dummy
        Yr  =(0,1,1),      # dummy
        willing=False,
        direct=False
    )

    donor1.Yl = (1,1,1)

    donor2  = Pair(
        id=2,
        X   =(0,1,0),
        Yl  =(0,1,0),      # left‐lobe: A‐type, small
        Yr  =(0,1,1),      # right‐lobe: A‐type, large
        willing=True,
        direct=False
    )
    patient2 = Pair(
        id=11,
        X   =(0,1,1),      # A patient, large
        Yl  =(0,1,1),
        Yr  =(0,1,1),
        willing=False,
        direct=False
    )

    # 3) AB donor (b=(0,0)): can only give to AB patients
    donor3  = Pair(
        id=3,
        X   =(0,0,0),
        Yl  =(0,0,0),      # left‐lobe: AB, small
        Yr  =(0,0,1),      # right‐lobe: AB, large
        willing=True,
        direct=False
    )
    patient3 = Pair(
        id=12,
        X   =(1,0,1),      # B‐type patient (1,0), large
        Yl  =(1,0,1),
        Yr  =(1,0,1),
        willing=False,
        direct=False
    )

    expected = ['l', 'r', None]

    for donor, patient, exp in zip(
        (donor1, donor2, donor3),
        (patient1, patient2, patient3),
        expected
    ):
        result = transplant_type(donor, patient)
        print(f"donor {donor.id} → patient {patient.id}: got {result!r}, expected {exp!r}")
        assert result == exp, f"Mismatch: got {result}, expected {exp}"
