import json
import sys
import xml.etree.ElementTree as ET


def load_schedule(input_file):
    """Load Node -> Slot mapping from a JSON file."""
    with open(input_file, "r") as file:
        return json.load(file)


def create_schedule_xml(schedule):
    """
    Convert Node -> Slot mapping into a generic TDMA
    schedule XML representation.

    This is an integration prototype. The exact EMANE
    event schema must match the EMANE version/model
    used in the target environment.
    """
    root = ET.Element(
        "tdma_schedule",
        {
            "slot_duration_ms": "1"
        }
    )

    for node, slot in sorted(schedule.items()):
        ET.SubElement(
            root,
            "assignment",
            {
                "node": node,
                "slot": str(slot)
            }
        )

    return ET.ElementTree(root)


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python schedule_adapter.py "
            "<schedule.json>"
        )
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        schedule = load_schedule(input_file)

    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {input_file}")
        sys.exit(1)

    tree = create_schedule_xml(schedule)

    output_file = "part2_emane/generated_schedule.xml"

    tree.write(
        output_file,
        encoding="utf-8",
        xml_declaration=True
    )

    print("TDMA schedule XML generated successfully.")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()