import datetime, re
import os
import csv
from fillpdf import fillpdfs



def create_validation_report(type, soldiers, soldier_id=None, uic=None):
   # individual soldier
    if type == 'individual':
        soldier = soldiers[str(soldier_id)]
        # output file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        csv_file_path = f"{timestamp}-report-{soldier['last_name']}.csv"

        with open(csv_file_path, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header
            csv_writer.writerow(['Soldier Name', 'Document', 'Issue', 'Compliant'])
            validate_soldier_documents(soldier, soldier_id, csv_writer)
            print(f"Validation report saved as {csv_file_path}")


    # uic
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        csv_file_path = f"{timestamp}-report-{uic}.csv"
        with open(csv_file_path, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header
            csv_writer.writerow(['Soldier Name', 'Document', 'Issue', 'Compliant'])
            # iterate through soldiers in UIC
            for soldier_id, soldier in soldiers.items():
                if soldier['UIC'] == uic:  
                    validate_soldier_documents(soldier, soldier_id, csv_writer)
                    
            print(f"Unit validation report saved as {csv_file_path}")



    return csv_file_path


def validate_soldier_documents(soldier, soldier_id, csv_writer):
    required_documents = [
    'DD Form 2760 - Qualification to Possess Firearms or Ammunition.pdf',
    'SGLV Form 8286.pdf',
    'SGLV Form 8286A.pdf',
    'DA Form 7425 - Readiness and Deployment Checklist.pdf'
    ]

    # iterate through each file for soldier
    soldier_folder = os.path.join("iPERMS", f"soldier_{soldier_id}")
    existing_files = set(os.listdir(soldier_folder))
    all_files = set(required_documents) | existing_files  
    
    for file in all_files:
        issues = None
        compliant = None
        # Check if the file is a required document
        if file in required_documents:
            if file not in existing_files:
                issues = "MISSING"
                compliant = "NO"
            else:
                # Validate the document (you can call your validation function here)
                file_path = os.path.join(soldier_folder, file)
                issues = validate_document(file_path, file, soldier)

                if issues == "N/A":
                    compliant = 'YES'
                elif issues == "Couldn't detect form fields":
                    compliant = "UNKNOWN"
                else:
                    compliant = "NO"
        else:
            # For extra files not in the required list, validate them as well
            file_path = os.path.join(soldier_folder, file)
            issues = validate_document(file_path, file, soldier)

            # Determine compliance
            if issues == "N/A":
                compliant = 'YES'
            elif issues == "Couldn't detect form fields":
                compliant = "UNKNOWN"
            else:
                compliant = "NO"
        
        soldier_name = f"{soldier['first_name']} {soldier['last_name']}"
        csv_writer.writerow([soldier_name, file, issues, compliant])

def validate_document(file_path, file_name, soldier):
    result = 'N/A' 
    doc_fields = fillpdfs.get_form_fields(file_path)
    # cannot detect fields
    if len(doc_fields)==0:
        result = "Couldn't detect form fields"
    # use helper functions
    else:
        # DD FORM 2760
        if file_name == 'DD Form 2760 - Qualification to Possess Firearms or Ammunition.pdf':
            result = dd_form_2760_validation(doc_fields, soldier)

        # SGLV Form 8286
        if file_name == 'SGLV Form 8286.pdf':
            result = sglv_form_8286_validation(doc_fields, soldier)

        # SGLV Form 8286A
        if file_name == 'SGLV Form 8286A.pdf':
            result = sglv_form_8286A_validation(doc_fields, soldier)

        # DA Form 7425
        if file_name == 'DA Form 7425 - Readiness and Deployment Checklist.pdf':
            result = da_form_7425_validation(doc_fields, soldier)
        

    return result


# helper functions per document type
def da_form_7425_validation(fields, soldier):
    issues = []
    fields = {standardize_field_name(k): v for k, v in fields.items()}
    # there's a bug, so if no edits have been made, just return no issues
    if fields.get('NAME[0]', '') == '':
        return 'N/A'

    # name (first, middle, last)
    full_name = fields.get('NAME[0]', '')
    name_parts = [part.strip() for part in full_name.split(",")]
    if len(name_parts) == 3:
        last_name, first_name, middle_name = name_parts[0], name_parts[1], name_parts[2]
        if first_name != soldier['first_name']:
            issues.append(f"First name mismatch: Expected {soldier['first_name']}, but got {first_name}")
        if last_name != soldier['last_name']:
            issues.append(f"Last name mismatch: Expected {soldier['last_name']}, but got {last_name}")
        if  middle_name != soldier['middle_name']:
            issues.append(f"Middle name mismatch: Expected {soldier['middle_name']}, but got {middle_name}")
    else:
       issues.append(f"Invalid name format (expected: Last, First, Middle): {full_name}")
    # uic
    if soldier['UIC'] != fields.get('UIC[0]', ''):
         wrong_uic = fields.get('UIC[0]', '')
         issues.append(f"UIC mismatch: Expected {soldier['UIC']}, but got {wrong_uic}")

    # rank
    if soldier['rank'] != fields.get('RankGrade[0]', ''):
        wrong_rank = fields.get('RankGrade[0]', '')
        issues.append(f"Rank mismatch: Expected {soldier['rank']}, but got {wrong_rank}")

    # dob
    if soldier['DOB']!=fields.get('DATE_APP26[0]', ''):
         wrong_dob = fields.get('DATE_APP26[0]', '')
         issues.append(f"DOB mismatch: Expected {soldier['DOB']}, but got {wrong_dob}")

    return ", ".join(issues) if issues else 'N/A'

def sglv_form_8286_validation(fields, soldier):
    issues = []
    # name (first, middle, last)
    full_name = fields.get('Name', '')
    name_parts = [part.strip() for part in full_name.split(",")]
    if len(name_parts) == 3:
        first_name, middle_name, last_name = name_parts[0], name_parts[1], name_parts[2]
        if first_name != soldier['first_name']:
            issues.append(f"First name mismatch: Expected {soldier['first_name']}, but got {first_name}")
        if last_name != soldier['last_name']:
            issues.append(f"Last name mismatch: Expected {soldier['last_name']}, but got {last_name}")
        if  middle_name != soldier['middle_name']:
            issues.append(f"Middle name mismatch: Expected {soldier['middle_name']}, but got {middle_name}")
    else:
       issues.append(f"Invalid name format (expected: First, Middle, Last): {full_name}")
    # branch
    if soldier['branch'] != fields.get('Branch', ''):
         issues.append(f"Branch mismatch: Expected {soldier['branch']}, but got {fields.get('Branch', '')}")

    # rank
    if soldier['rank'] != fields.get('Rank', ''):
        issues.append(f"Rank mismatch: Expected {soldier['rank']}, but got {fields.get('Rank', '')}")

    # ssn
    if soldier['SSN']!=fields.get('ss', ''):
         issues.append(f"SSN mismatch: Expected {soldier['SSN']}, but got {fields.get('ss', '')}")

    return ", ".join(issues) if issues else 'N/A'

def sglv_form_8286A_validation(fields, soldier):
    issues = []
    # name (first, middle, last)
    full_name = fields.get('sm_name', '')
    name_parts = [part.strip() for part in full_name.split(",")]
    if len(name_parts) == 3:
        first_name, middle_name, last_name = name_parts[0], name_parts[1], name_parts[2]
        if first_name != soldier['first_name']:
            issues.append(f"First name mismatch: Expected {soldier['first_name']}, but got {first_name}")
        if last_name != soldier['last_name']:
            issues.append(f"Last name mismatch: Expected {soldier['last_name']}, but got {last_name}")
        if  middle_name != soldier['middle_name']:
            issues.append(f"Middle name mismatch: Expected {soldier['middle_name']}, but got {middle_name}")
    else:
       issues.append(f"Invalid name format (expected: First, Middle, Last): {full_name}")
    # branch
    if soldier['branch'] != fields.get('sm_branch', ''):
         issues.append(f"Branch mismatch: Expected {soldier['branch']}, but got {fields.get('sm_branch', '')}")

    # sp ssn
    if soldier['spouse_SSN'] != fields.get('sp_ss', ''):
        issues.append(f"Spouse SSN mismatch: Expected {soldier['spouse_SSN']}, but got {fields.get('sp_ss', '')}")

    # ssn
    if soldier['SSN']!=fields.get('sm_ss', ''):
         issues.append(f"SSN mismatch: Expected {soldier['SSN']}, but got {fields.get('sm_ss', '')}")

    return ", ".join(issues) if issues else 'N/A'


def dd_form_2760_validation(fields, soldier):
    fields = {standardize_field_name(k): v for k, v in fields.items()}
    issues = []
    # name
    full_name = fields.get('Name[0]', '')
    parts = [part.strip() for part in full_name.split(",")]
    # Ensure there are exactly three parts (last name, first name, middle initial)
    if len(parts) == 3:
        last_name, first_name, middle_initial = parts[0], parts[1], parts[2]
        if first_name != soldier['first_name']:
            issues.append(f"First name mismatch: Expected {soldier['first_name']}, but got {first_name}")
        if last_name != soldier['last_name']:
            issues.append(f"Last name mismatch: Expected {soldier['last_name']}, but got {last_name}")
        if  middle_initial != soldier['middle_name'][0]:
            issues.append(f"Middle initial mismatch: Expected {soldier['middle_name'][0]}, but got {middle_initial}")
    else:
       issues.append(f"Invalid name format (expected: Last, First, Middle Initial): {full_name}")

    # uic
    if soldier['UIC']!=fields.get('Org[0]', ''):
         issues.append(f"UIC mismatch: Expected {soldier['UIC']}, but got {fields.get('Org[0]', '')}")

    # rank
    if soldier['rank']!=fields.get('RankGrade[0]', ''):
         issues.append(f"Rank mismatch: Expected {soldier['rank']}, but got {fields.get('RankGrade[0]', '')}")

    # ssn
    if soldier['SSN']!=fields.get('SSN[0]', ''):
         issues.append(f"SSN mismatch: Expected {soldier['SSN']}, but got {fields.get('SSN[0]', '')}")
    
    return ", ".join(issues) if issues else 'N/A'


def standardize_field_name(field_name):
    # This regex will match patterns like '\\1330\\135' and remove or replace them
    standardized_name = re.sub(r'\\\d+\\\d+', '[0]', field_name)  # Replace with [0] or another pattern
    return standardized_name