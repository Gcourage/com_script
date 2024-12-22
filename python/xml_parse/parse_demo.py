import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('/Users/hubinbin/codes/exam/utils/demo.xml')
root = tree.getroot()

# Find all 'test_run' elements
test_runs = root.findall(".//test_run")

# Create a list to store the 'test_run' elements
test_run_list = []

# Iterate over each 'test_run' element and append it to the list
for test_run in test_runs:
    print(f"{test_run.attrib['name']}, {test_run.attrib['status']}")
    test_run_list.append(test_run)
