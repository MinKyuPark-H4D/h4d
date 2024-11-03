
import os, shutil
from datetime import datetime
from fillpdf import fillpdfs
import PyPDF2
import pandas as pd



def fill_in_sglv(folder, INFO):
    print('Filling in SGLV Form 8286...')
    data_dict = {'Name': f"{INFO['first_name']}, {INFO['middle_name']}, {INFO['last_name']}",
                 'Rank': INFO['rank'], 'Branch':INFO['branch'], 'ss':INFO['SSN'], 
                 'servicemember ss':INFO['SSN'], 'servicemember address':INFO['address'],
        'spouse name':INFO['spouse_name'], 'spouse dob':INFO['spouse_dob']}

    fillpdfs.write_fillable_pdf('./document-templates/SGLV Form 8286.pdf', f'{folder}/SGLV Form 8286.pdf', data_dict)
    print('Completed')

def fill_in_sglv_a(folder, INFO):
    print('Filling in SGLV Form 8286A...')
    data_dict = {'sm_name': f"{INFO['first_name']}, {INFO['middle_name']}, {INFO['last_name']}",
                'sm_branch':INFO['branch'], 'sm_ss':INFO['SSN'], 'sp_address':INFO['address'],
        'sp_name':INFO['spouse_name'], 'sp_dob':INFO['spouse_dob'], 'sp_ss':INFO['spouse_SSN']}

    fillpdfs.write_fillable_pdf('./document-templates/SGLV Form 8286A.pdf', f'{folder}/SGLV Form 8286A.pdf', data_dict)
    print('Completed')

def fill_in_2760(folder, INFO):
    print('Filling in DD Form 2760 - Qualification to Possess Firearms or Ammunition')
    today = datetime.today()
    formatted_date = today.strftime("%Y%m%d")
    try:
        with open('./document-templates/DD Form 2760 - Qualification to Possess Firearms or Ammunition.pdf', 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            writer = PyPDF2.PdfWriter()
         
            page = pdf_reader.pages[0]
            writer.add_page(page)
            data_dict = {f'Name[0]':f"{INFO['last_name']}, {INFO['first_name']}, {INFO['middle_name'][0]}", f'RankGrade[0]':INFO['rank'],
                        f'SSN[0]':INFO['SSN'],  f'Org[0]':INFO['UIC'], f'signedDate[0]':formatted_date,}
            writer.update_page_form_field_values(
                writer.pages[0], data_dict
            )
                
            with open(f'{folder}/DD Form 2760 - Qualification to Possess Firearms or Ammunition.pdf', "wb") as output_stream:
                writer.write(output_stream)
           
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF: {e}")
  
    print('Completed')

def fill_in_7425(folder, INFO):
    print('Fillling in DA Form 7425 - Readiness and Deployment Checklist')
    formatted_date = datetime.today().strftime("%Y%m%d")
    try:
        with open('./document-templates/DA Form 7425 - Readiness and Deployment Checklist.pdf', 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            writer = PyPDF2.PdfWriter()
            count = len(pdf_reader.pages)

            for i in range(count):
                page = pdf_reader.pages[i]
                writer.add_page(page)
                if i == 0:
                    data_dict = {f'NAME[{i}]':f"{INFO['last_name']}, {INFO['first_name']}, {INFO['middle_name']}", f'RankGrade[{i}]':INFO['rank'],
                                f'DATE_APP26[{i}]':INFO['DOB'],  f'UIC[{i}]':INFO['UIC'], f'DATE_APP[{i}]':formatted_date, f'Soldier_Email[{i}]':INFO['email']}
                    writer.update_page_form_field_values(
                        writer.pages[i], data_dict
                    )
                elif i==2:
                    data_dict = {f'NAME{i}[0]':f"{INFO['last_name']}, {INFO['first_name']}, {INFO['middle_name']}", f'RankGrade5[0]':INFO['rank'],
                    'DATE2[0]':formatted_date, f'UIC29[0]':INFO['UIC']}
                    writer.update_page_form_field_values(
                        writer.pages[i], data_dict
                    )
                
            with open(f'{folder}/DA Form 7425 - Readiness and Deployment Checklist.pdf', "wb") as output_stream:
                writer.write(output_stream)
           
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF: {e}")
  
    print('Completed')


def main():
    df = pd.read_csv('fake-soldier-data.csv', index_col=False)
   
    for index, row in df.iterrows():
        INFO = {
            'last_name': row['last_name'],
            'first_name': row['first_name'],
            'middle_name': row['middle_name'],
            'UIC': row['UIC'],
            'DOB': row['DOB'],
            'rank': row['rank'],
            'branch': row['branch'],
            'email': row['email'],
            'SSN': row['SSN'],
            'address': row['address'],
            'spouse_name': row['spouse_name'],
            'spouse_dob': row['spouse_dob'],
            'spouse_SSN': row['spouse_SSN']
        }

        new_folder = f"./autofilled-documents/{INFO['last_name']}-{INFO['first_name']}-{INFO['UIC']}"
        if os.path.exists(new_folder):
            shutil.rmtree(new_folder)
        os.makedirs(new_folder)
        print(f"Creating documents for {INFO['first_name']}-{INFO['last_name']}-{INFO['UIC']}")
        fill_in_sglv(new_folder, INFO)
        fill_in_sglv_a(new_folder, INFO)
        fill_in_2760(new_folder, INFO)
        fill_in_7425(new_folder, INFO)
        print('Completed')
        print('-----------')


if __name__ == '__main__':
    main()