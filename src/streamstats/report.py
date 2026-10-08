import json


def get_top_sources(report_data: dict) -> list:
    sorted_sources = sorted(
        report_data.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return sorted_sources

def write_report(report_data: dict, error_critical: dict, output_file, top_n: int = 5):
    top = get_top_sources(error_critical)

    if top_n < len(top):
        top = top[:top_n]

    report_data["top_ERROR|CRITICAL_sources"] = [
        {"sources": sources, "count": count}
        for sources, count in top
    ]

    if output_file == '-':
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
    else:
        with open(output_file, 'w', encoding='utf8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
