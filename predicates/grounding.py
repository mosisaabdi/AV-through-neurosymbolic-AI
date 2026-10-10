PREDICATE_NAMES = (
    "red_signal", "at_stop_line", "pedestrian_in_crosswalk",
    "obstacle_on_drivable_area", "speed_limit_applicable",
    "speed_above_limit", "lane_available"
)

def _truth(value, name):
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return float(value)
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0,1]")
    return value

def ground_predicates(scene):
    """Read pre-grounded values; real perception-to-predicate functions are TODO."""
    raw = scene.get("predicates", {})
    return {name: _truth(raw.get(name, 0.0), name) for name in PREDICATE_NAMES}
