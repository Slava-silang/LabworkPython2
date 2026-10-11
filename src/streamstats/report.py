import json


def get_top_sources(report_data: dict) -> list:
    """The function for sorting ERROR|CRITICAL sources"""
    sorted_sources = sorted(
        report_data.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return sorted_sources # Return result of sorting

def write_report(report_data: dict, error_critical: dict, output_file, top_n: int = 5):
    """The function for writing reports"""
    top = get_top_sources(error_critical) # Get top ERROR|CRITICAL sources

    if top_n < len(top):
        top = top[:top_n] # Check whether count of sources if bigger than top_n to avoid exceptions

    report_data["top_ERROR|CRITICAL_sources"] = [ # Add ERROR|CRITICAL sources to main data
        {"sources": sources, "count": count}
        for sources, count in top
    ]

    if output_file == '-': # Write data to stdout if there is no output file
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
    else: # Write data to output file
        with open(output_file, 'w', encoding='utf8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
