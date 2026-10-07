import json

def write_report(report_data, output_file):
    """
    Write the report data to a JSON file.

    Args:
        report_data (dict): The report data to write.
        output_file (str): The path to the output JSON file.
    """
    if output_file == '-':
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
    else:
        with open(output_file, 'w', encoding='utf8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)