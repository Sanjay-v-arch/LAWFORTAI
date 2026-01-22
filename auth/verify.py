def verify_police_id(police_id: str) -> bool:
    return police_id and police_id.startswith("POL")

def verify_lawyer_id(lawyer_id: str) -> bool:
    return lawyer_id and lawyer_id.startswith("BAR")
