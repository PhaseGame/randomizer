import argparse
import os
import sys
import importlib.util
from typing import List


def get_repo_root_directory() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_src_directory() -> str:
    return os.path.join(get_repo_root_directory(), "src")


def get_events_directory() -> str:
    return os.path.join(get_src_directory(), "events")


def list_available_events() -> List[str]:
    events_root = get_events_directory()
    if not os.path.isdir(events_root):
        return []
    event_names: List[str] = []
    for entry in os.listdir(events_root):
        event_dir = os.path.join(events_root, entry)
        if os.path.isdir(event_dir) and os.path.isfile(os.path.join(event_dir, "select_winners.py")):
            event_names.append(entry)
    event_names.sort()
    return event_names


def load_event_module(event_name: str):
    src_dir = get_src_directory()
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    event_script_path = os.path.join(get_events_directory(), event_name, "select_winners.py")
    if not os.path.isfile(event_script_path):
        available = list_available_events()
        available_hint = ", ".join(available) if available else "<no events found>"
        raise FileNotFoundError(
            f"Event '{event_name}' not found. Expected script at: {event_script_path}. "
            f"Available events: {available_hint}"
        )

    module_name = f"event_{event_name.replace('-', '_')}_select_winners"
    spec = importlib.util.spec_from_file_location(module_name, event_script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create module spec for event script: {event_script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a prize selection event")
    parser.add_argument("event", type=str, help="Event directory name under src/events, e.g., 'durov-glasses-20-aug'")
    parser.add_argument("--seed", type=int, required=True, help="Random seed (from dice)")
    args = parser.parse_args()

    event_module = load_event_module(args.event)
    if not hasattr(event_module, "main"):
        raise AttributeError("Selected event script does not expose a 'main(seed: Optional[int])' function")

    event_module.main(args.seed)


if __name__ == "__main__":
    main()


