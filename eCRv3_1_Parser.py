import os
import sys
import pandas as pd
from lxml import etree
import zipfile
import glob
import csv
import datetime
import time

def set_wdir(wdir):
    
    cwd = os.getcwd()

    try:     
        os.chdir(wdir)
        print('Working directory change was successful')
    except:
        print("Something went wrong")
        print(sys.exc_info())
    finally:
        print(f'Your current working directory is: {os.getcwd()}')


def printException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(f'EXCEPTION IN ({filename}, LINE {lineno} "{line.strip()}"): {exc_obj}')


today = datetime.datetime.now()

yesterday = today - datetime.timedelta(days=1)

year = str(yesterday.strftime("%Y"))
print(year)
month = str(yesterday.strftime("%m"))
print(month)
day = str(yesterday.strftime("%d"))
print(day)

eICR_file_path = "" ## Put filepath to zip files here

output_path = "" ## Put where you want the output file to go. This could be switched to having the data placed in a database, but will require code updates.

myDate = year + month + day

print(myDate)

startTime = time.time()
if os.path.exists(f"{eICR_file_path}\\{year}{month}{day}_zip.csv"):
    print("File Exists")
else:
    with open(f"{eICR_file_path}\\{year}{month}{day}_zip.csv", mode = 'w', newline = '') as file: ## This opens/creates a csv file and adds the headers to the file
        writer =  csv.writer(file)
        writer.writerow(['doc_oid_root', 'doc_oid_ext', 'doc_oid_assigningauthor', 'set_id_root', 'set_id_ext', 'set_id_assigningAuthor',
                         'effective_time', 'vcn', 'legal_given_names', 'given_names', 'legal_family_names', 'family_names',
                         'patient_address_street', 'patient_address_city', 'patient_address_state', 'patient_address_zip', 'patient_address_county', 'patient_address_country',
                         'patient_telecoms', 'patient_telecom_uses', 'patient_dob', 'patient_race_code', 'patient_race_code_system', 'patient_race_name',
                         'patient_ethnicity_code', 'patient_ethnicity_code_system', 'patient_ethnicity_name', 'patient_gender_code', 'patient_gender_code_system', 'patient_gender_name',
                         'patient_marital_code', 'patient_marital_code_system', 'patient_marital_name', 'patient_language', 'patient_pregnant1', 'patient_pregnant2',
                         'patient_deceased', 'patient_mrn', 'patient_smoking', 'patient_tobacco', 'patient_alcohol', 'patient_immunization_status',
                         'patient_ssn1', 'patient_ssn2', 'guardian_presence', 'guardian_given_names', 'guardian_family_name', 'guardian_street',
                         'guardian_city', 'guardian_state', 'guardian_zip', 'guardian_county', 'guardian_country', 'guardian_telecom_value',
                         'guardian_telecom_use', 'travel_history_location1', 'travel_history_location2', 'travel_history_low',
                         'travel_history_high', 'hco_root', 'hco_extension', 'hco_name', 'hco_telecom_use', 'hco_telecom_value',
                         'hco_street', 'hco_city', 'hco_state', 'hco_zip', 'hco_county', 'hco_country', 'facility_root', 'facility_extension',
                         'facility_name', 'facility_street', 'facility_city', 'facility_state', 'facility_zip', 'facility_county',
                         'facility_country', 'provider_given_name', 'provider_family_name', 'provider_root', 'provider_extension',
                         'provider_telecom_use', 'provider_telecom_value', 'provider_street', 'provider_city', 'provider_state',
                         'provider_zip', 'provider_county', 'provider_country', 'software', 'software_version', 'encompassing_encounter',
                         'encompassing_encounter_code', 'discharge_disposition', 'encounter_time', 'misc_notes', 'abort_med',
                         'pregSupTimeLow', 'pregSupTimeHigh', 'pregSupDetMethodCode', 'pregSupDetMethodCodeSystem', 'pregSupDetMethodDisplay',
                         'pregSupRecordDate', 'pregSupEstDelivDate', 'pregSupDelivDateMethodCode', 'pregSupDelivDateMethodCodeSystem',
                         'pregSupDelivDateMethodDisplay', 'patGenderIdentityCode', 'patGenderIdentityCodeSystem', 'patGenderIdentityCode',
                         'pregSupLastMenst', 'pregSupOutcomeCode', 'pregSupOutcomeCodeSystem', 'pregSupOutcomeDisplay', 'pregSupOutcomeTime',
                         'PregSupPostPartStatusCode', 'PregSupPostPartStatusCodeSystem', 'PregSupPostPartStatusDisplay', 'resultOrgTriggerCode',
                         'resultOrgTriggerCodeSystem', 'resultOrgTriggerDisplay', 'medAdminTriggerCode','medAdminTriggerCodeSystem',
                         'medAdminTriggerDisplay', 'medPlannedCode', 'medPlannedCodeSystem', 'medPlannedDisplay',
                         'medPlannedTriggerCode', 'medPlannedTriggerCodeSystem', 'medPlannedTriggerDisplay', 'medCodeCode', 'medCodeCodeSystem',
                         'medCodeDisplay', 'medTriggerCode', 'medTriggerCodeSystem', 'medTriggerDisplay', 'immuVaccTrigCode', 'immuVaccTrigCodeSystem',
                         'immuVaccTrigDisplay', 'travelPurpCode', 'travelPurpCodeSystem', 'travelPurpDisplay', 'travelTypeCode', 'travelTypeCodeSystem',
                         'travelTypeDisplay', 'travelTransDetailCode', 'travelTransDetailCodeSystem', 'travelTransDetailDisplay', 'travelTransDetailValue',
                         'occupationCurrentCode', 'occupationCurrentCodeSystem', 'occupationCurrentDisplay', 'occupationUsualCode', 'occupationUsualCodeSystem', 'occupationUsualDisplay',
                         'industryCurrentCode', 'industryCurrentCodeSystem', 'industryCurrentDisplay', 'industryUsualCode', 'industryUsualCodeSystem', 'industryUsualDisplay', 'currentEmployerName', 'currentEmployerPhone',
                         'currentEmployerAddressStreet', 'currentEmployerAddressCounty', 'currentEmployerAddressCity','currentEmployerAddressState',
                         'currentEmployerAddressZip', 'currentEmployerAddressCountry', 'ocupationExposure', 'EmploymentStatusCode', 'EmploymentStatusCodeSystem', 'EmploymentStatusDisplay',
                         'pregSupEstGestAge', 'pregSupEstGestAgeDate', 'pregSupEstGestAgeMethodCode', 'pregSupEstGestAgeMethodCodeSystem',  'pregSupEstGestAgeMethodDisplay',
                         'medHistCode', 'medHistCodeSystem', 'medHistDisplay', 'medHistText', 'systemsReviewText', 'specimenSourceCode', 'specimenSourceCodeSystem',
                         'specimenSourceDisplay', 'specimenTypeCode', 'specimenId', 'specimentCollectDate', 'vitalsValue', 'vitalsUse', 'medTherRespValueCode', 'medTherRespValueCodeSystem', 'medTherRespValueDisplay', 'homelessFlag',
                         'procActCode', 'procActCodeSystem', 'procActCodeDisplay', 'procObsCode', 'procObsCodeSystem', 'procObsDisplay', 'procCode',
                         'procCodeSystem', 'procDisplay', 'procTriggerActCode', 'procTriggerActCodeSystem', 'procTriggerActDisplay', 'procTriggerObsCode',
                         'procTriggerObsCodeSystem', 'procTriggerObsDisplay', 'procTriggerProcCode', 'procTriggerProcCodeSystem', 'procTriggerProcDisplay',
                         'procPlannedActCode', 'procPlannedActCodeSystem', 'procPlannedActDisplay', 'procPlannedProcCode', 'procPlannedProcCodeSystem', 'procPlannedProcDisplay',
                         'procPlannedObsCode', 'procPlannedObsCodeSystem', 'procPlannedObsDisplay',
                         'procPlannedTrigObsCode', 'procPlannedTrigObsCodeSystem', 'procPlannedTrigObsDisplay', 'procPlannedTriggerProcCode', 'procPlannedTriggerProcCodeSystem',
                         'procPlannedTriggerProcDisplay', 'disabilityStatusCode', 'disabilityStatusCodeSystem', 'disabilityStatusDisplay', 'emergencyOutbreakCode',
                         'emergencyOutbreakCodeSystem', 'emergencyOutbreakDisplay', 'exposureInfoCode', 'exposureInfoCodeSystem', 'exposureInfoDisplay', 'tribalAffiliationCode',
                         'tribalAffiliationCodeSystem', 'tribalAffiliationDisplay', 'vaccineCredPatAssertCode', 'vaccineCredPatAssertCodeSystem', 'vaccineCredPatAssertDisplay',
                         'nationalityCountryCode', 'nationalityCountryCodeSystem', 'nationalityCountryDisplay', 'residenceCountryCode', 'residenceCountryCodeSystem', 'residenceCountryCodeDisplay'])
        print("File Prepped")



ns = {'n':"urn:hl7-org:v3",
      'cda':"urn:hl7-org:v3",
      'sdtc':"urn:hl7-org:sdtc", 
      'xsi':"http://www.w3.org/2001/XMLSchema-instance"}


print(f"{eICR_file_path}\\{year}\\{year}{month}\\{myDate}")
set_wdir(f"{eICR_file_path}\\{year}\\{year}{month}\\{myDate}")
cwd = os.getcwd()
#print(cwd)

extract_location = ''  ## Place teporary location for extracted files will be rewritten, I used a tmp folder, the data here is continuously overwritten, may want to add logic to remove the unzipped files at the end of the script

cdaLocation = f"{extract_location}\\CDA_eICR.xml"

zipfold = f"{eICR_file_path}\\{year}\\{year}{month}\\{myDate}"

for root, dirs, files in os.walk(cwd, topdown = False):
    #print(root,dirs,files)
    if root == zipfold:
        for file in files:
            filePath = os.path.join(zipfold, file)
            #print(filePath)
            if filePath[-4:] == ".zip":
                try:
                    with zipfile.ZipFile(filePath, 'r') as zip_ref:
                        zip_ref.extractall(extract_location)

                    tree = etree.parse(cdaLocation)
                    root = tree.getroot()

                    doc_oid_root_path = '/n:ClinicalDocument/n:id/@root'
                    doc_oid_ext_path = '/n:ClinicalDocument/n:id/@extension'
                    doc_oid_assigningAuthor_path = '/n:ClinicalDocument/n:id/@assigningAuthorityName'

                    doc_oid_root = ';'.join(tree.xpath(doc_oid_root_path, namespaces = ns))
                    doc_oid_ext = ';'.join(tree.xpath(doc_oid_ext_path, namespaces = ns))
                    doc_oid_assigningauthor = ';'.join(tree.xpath(doc_oid_assigningAuthor_path, namespaces = ns))

                    print(doc_oid_root, doc_oid_ext, doc_oid_assigningauthor)

                    set_id_root_path = '/n:ClinicalDocument/n:setId/@root'
                    set_id_ext_path = '/n:ClinicalDocument/n:setId/@extension'
                    set_id_assigningAuthor_path = '/n:ClinicalDocument/n:setId/@assigningAuthorityName'

                    set_id_root = ';'.join(tree.xpath(set_id_root_path, namespaces = ns))
                    set_id_ext = ';'.join(tree.xpath(set_id_ext_path, namespaces=ns))
                    set_id_assigningAuthor = ';'.join(tree.xpath(set_id_assigningAuthor_path, namespaces=ns))

                    print(set_id_root, set_id_ext, set_id_assigningAuthor)

                    effective_time_path = '/n:ClinicalDocument/n:effectiveTime/@value'

                    effective_time = ';'.join(tree.xpath(effective_time_path, namespaces = ns))

                    print(effective_time)

                    vcn_path = '/n:ClinicalDocument/n:versionNumber/@value'

                    vcn = ';'.join(tree.xpath(vcn_path, namespaces = ns))

                    print(vcn)

                    ## Collect patient names
                    legal_given_names_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:name[@use="L"]/n:given/text()'
                    legal_given_names = ';'.join(tree.xpath(legal_given_names_path, namespaces = ns))

                    print(legal_given_names)

                    given_names_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:name/n:given/text()"
                    given_names = ';'.join(tree.xpath(given_names_path, namespaces= ns))

                    print(given_names)

                    legal_family_names_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:name[@use='L']/n:family/text()"
                    legal_family_names = ';'.join(tree.xpath(legal_family_names_path, namespaces = ns))

                    print(legal_family_names)

                    family_names_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:name/n:family/text()"
                    family_names = ';'.join(tree.xpath(family_names_path, namespaces=ns))

                    print(family_names)

                    ## Collect patient address
                    patient_address_street_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:addr/n:streetAddressLine/text()"
                    patient_address_city_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:addr/n:city/text()"
                    patient_address_state_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:addr/n:state/text()"
                    patient_address_zip_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:addr/n:postalCode/text()"
                    patient_address_county_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:addr/n:county/text()"
                    patient_address_country_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:addr/n:country/text()"

                    patient_address_street = ';'.join(tree.xpath(patient_address_street_path, namespaces=ns))
                    patient_address_city = ';'.join(tree.xpath(patient_address_city_path, namespaces=ns))
                    patient_address_state = ';'.join(tree.xpath(patient_address_state_path, namespaces=ns))
                    patient_address_zip = ';'.join(tree.xpath(patient_address_zip_path, namespaces=ns))
                    patient_address_county = ';'.join(tree.xpath(patient_address_county_path, namespaces=ns))
                    patient_address_country = ';'.join(tree.xpath(patient_address_country_path, namespaces=ns)) ## Creates a concatenated value with ";" as the delimiter should there be multiple addresses

                    print(patient_address_street, patient_address_city, patient_address_state, patient_address_zip, patient_address_county, patient_address_country)

                    ## Patient Telecom Info
                    patient_telecom_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:telecom/@value'
                    patient_telecom_use_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:telecom/@use'

                    patient_telecoms =';'.join(tree.xpath(patient_telecom_path, namespaces=ns))
                    patient_telecom_uses =';'.join(tree.xpath(patient_telecom_use_path, namespaces=ns))

                    print(patient_telecoms, patient_telecom_uses)

                    ## Patient DOB
                    patient_dob_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:birthTime/@value'

                    patient_dob =';'.join(tree.xpath(patient_dob_path, namespaces=ns))
                    print(patient_dob)

                    ## Patient Race
                    patient_race_code_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:raceCode/@code'
                    patient_race_code_system_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:raceCode/@codeSystem'
                    patient_race_name_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:raceCode/@displayName'

                    patient_race_code =';'.join(tree.xpath(patient_race_code_path, namespaces=ns))
                    patient_race_code_system =';'.join(tree.xpath(patient_race_code_system_path, namespaces=ns))
                    patient_race_name =';'.join(tree.xpath(patient_race_name_path, namespaces=ns))

                    print(patient_race_code, patient_race_name)

                    ## Patient Ethnicity
                    patient_ethnicity_code_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:ethnicGroupCode/@code'
                    patient_ethnicity_code_system_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:ethnicGroupCode/@codeSystem'
                    patient_ethnicity_name_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:ethnicGroupCode/@displayName'

                    patient_ethnicity_code =';'.join(tree.xpath(patient_ethnicity_code_path, namespaces=ns))
                    patient_ethnicity_code_system =';'.join(tree.xpath(patient_ethnicity_code_system_path, namespaces=ns))
                    patient_ethnicity_name =';'.join(tree.xpath(patient_ethnicity_name_path, namespaces=ns))

                    print(patient_ethnicity_code, patient_ethnicity_name)

                    ## Patient Gender
                    patient_gender_code_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:administrativeGenderCode/@code'
                    patient_gender_code_system_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:administrativeGenderCode/@codeSystem'
                    patient_gender_name_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:administrativeGenderCode/@displayName'

                    patient_gender_code =';'.join(tree.xpath(patient_gender_code_path, namespaces=ns))
                    patient_gender_code_system =';'.join(tree.xpath(patient_gender_code_system_path, namespaces=ns))
                    patient_gender_name =';'.join(tree.xpath(patient_gender_name_path, namespaces=ns))

                    print(patient_gender_code, patient_gender_name)

                    ## Patient Marital Status
                    patient_marital_code_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:maritalStatusCode/@code'
                    patient_marital_code_system_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:maritalStatusCode/@codeSystem'
                    patient_marital_name_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:maritalStatusCode/@displayName'

                    patient_marital_code =';'.join(tree.xpath(patient_marital_code_path, namespaces=ns))
                    patient_marital_code_system =';'.join(tree.xpath(patient_marital_code_system_path, namespaces=ns))
                    patient_marital_name =';'.join(tree.xpath(patient_marital_name_path, namespaces=ns))

                    print(patient_marital_code, patient_marital_name)

                    ## Patient Language
                    patient_language_code_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:languageCommunication/n:languageCode/@code'
                    patient_language_code_system_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:languageCommunication/n:languageCode/@codeSystem'
                    patient_language_name_path = '/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:languageCommunication/n:languageCode/@displayName'

                    patient_language_code =';'.join(tree.xpath(patient_language_code_path, namespaces=ns))
                    patient_language_code_system =';'.join(tree.xpath(patient_language_code_system_path, namespaces=ns))
                    patient_language_name =';'.join(tree.xpath(patient_language_name_path, namespaces=ns))

                    print(patient_language_code)

                    ## Patient Pregnant
                    patient_pregnant_path1 = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:act/n:entryRelationship/n:observation[n:code/n:translation/@code='29308-4']/n:value/@code=77386006"
                    patient_pregnant_path2 = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.3.8']/n:value/@code"

                    patient_pregnant1 = tree.xpath(patient_pregnant_path1, namespaces=ns)
                    patient_pregnant2 =';'.join(tree.xpath(patient_pregnant_path2, namespaces=ns))

                    print(patient_pregnant1, patient_pregnant2)

                    ## Patient Deceased
                    patient_deceased_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/sdtc:deceasedInd/@value"

                    patient_deceased =';'.join(tree.xpath(patient_deceased_path, namespaces=ns))

                    print(patient_deceased)

                    ## Patient MRN
                    patient_mrn_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:id[@root!='2.16.840.1.113883.4.1']/@extension"

                    patient_mrn =';'.join(tree.xpath(patient_mrn_path, namespaces=ns))

                    print(patient_mrn)

                    ## patient smoking status
                    patient_smoking_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.78']/n:value/@displayName"

                    patient_smoking =';'.join(tree.xpath(patient_smoking_path, namespaces=ns))

                    print(patient_smoking)

                    ## patient tobacco status
                    patient_tobacco_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:observation[n:code/n:translation/@code='88031-0']/n:value/@displayName"

                    patient_tobacco =';'.join(tree.xpath(patient_tobacco_path, namespaces=ns))

                    print(patient_tobacco)

                    ## patient alcohol use
                    patient_alcohol_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:observation[n:code/n:translation/@code='11331-6']/n:value/@displayName"

                    patient_alcohol =';'.join(tree.xpath(patient_alcohol_path, namespaces=ns))

                    print(patient_alcohol)

                    ## patient immunization status
                    patient_immunization_status_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:substanceAdministration[n:templateId/@root='2.16.840.1.113883.10.20.22.4.52']/n:statusCode/@code"

                    patient_immunization_status =';'.join(tree.xpath(patient_immunization_status_path, namespaces=ns))

                    print(patient_immunization_status)

                    ## patient ssn
                    patient_ssn_path1 = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:id[@root='2.16.840.1.113883.4.1']/@extension"
                    patient_ssn_path2 = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:id[@assigningAuthorityName='Social Security Administration']/@extension"

                    patient_ssn1 =';'.join(tree.xpath(patient_ssn_path1, namespaces=ns))
                    patient_ssn2 =';'.join(tree.xpath(patient_ssn_path2, namespaces=ns))

                    print(patient_ssn1, patient_ssn2)

                    ## Guardian information
                    ### guardian presence
                    guardian_presence_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian"

                    guardian_presence = len(tree.xpath(guardian_presence_path, namespaces=ns))

                    print(guardian_presence)

                    ### Guardian given name
                    guardian_given_name_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:guardianPerson/n:name/n:given/text()"

                    guardian_given_names =';'.join(tree.xpath(guardian_given_name_path, namespaces=ns))

                    print(guardian_given_names)

                    ### guardian family name
                    guardian_family_name_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:guardianPerson/n:name/n:family/text()"

                    guardian_family_name =';'.join(tree.xpath(guardian_family_name_path, namespaces=ns))

                    print(guardian_family_name)

                    ### guardian street address
                    guardian_street_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:addr/n:streetAddressLine/text()"

                    guardian_street =';'.join(tree.xpath(guardian_street_path, namespaces=ns))

                    print(guardian_street)

                    ### guardian city
                    guardian_city_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:addr/n:city/text()"

                    guardian_city =';'.join(tree.xpath(guardian_city_path, namespaces=ns))

                    print(guardian_city)

                    ### Guardian state
                    guardian_state_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:addr/n:state/text()"

                    guardian_state =';'.join(tree.xpath(guardian_state_path, namespaces=ns))

                    print(guardian_state)

                    ### guardian zip
                    guardian_zip_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:addr/n:postalCode/text()"

                    guardian_zip =';'.join(tree.xpath(guardian_zip_path, namespaces=ns))

                    print(guardian_zip)

                    ### guardian county
                    guardian_county_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:addr/n:county/text()"

                    guardian_county =';'.join(tree.xpath(guardian_county_path, namespaces=ns))

                    print(guardian_county)

                    ### guardian country
                    guardian_country_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:addr/n:country/text()"

                    guardian_country =';'.join(tree.xpath(guardian_country_path, namespaces=ns))

                    print(guardian_country)

                    ### guardian telecom value
                    guardian_telecom_value_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:telecom/@value"

                    guardian_telecom_value =';'.join(tree.xpath(guardian_telecom_value_path, namespaces=ns))

                    print(guardian_telecom_value)

                    ### guardian telecom use
                    guardian_telecom_use_path = "/n:ClinicalDocument/n:recordTarget/n:patientRole/n:patient/n:guardian/n:telecom/@use"

                    guardian_telecom_use =';'.join(tree.xpath(guardian_telecom_use_path, namespaces=ns))

                    print(guardian_telecom_use)

                    ### Travel History
                    travel_history_location1_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:act[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.1']/n:text/text()"
                    travel_history_location2_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:act[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.1']/n:participant/n:participantRole/n:code/@displayName"

                    travel_history_location1 =';'.join(tree.xpath(travel_history_location1_path, namespaces=ns))
                    travel_history_location2 =';'.join(tree.xpath(travel_history_location2_path, namespaces=ns))

                    print(travel_history_location1, travel_history_location2)

                    ### travel history low
                    travel_history_low_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:act[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.1']/n:effectiveTime/n:low/@value"

                    travel_history_low =';'.join(tree.xpath(travel_history_low_path, namespaces=ns))

                    print(travel_history_low)

                    ### travle hisotry high
                    travel_history_high_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:act[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.1']/n:effectiveTime/n:high/@value"

                    travel_history_high =';'.join(tree.xpath(travel_history_high_path, namespaces=ns))

                    print(travel_history_high)

                    ### HCO root
                    hco_root_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:id/@root"

                    hco_root =';'.join(tree.xpath(hco_root_path, namespaces=ns))

                    print(hco_root)

                    ### HCO extension
                    hco_extension_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:id/@extension"

                    hco_extension =';'.join(tree.xpath(hco_extension_path, namespaces=ns))

                    print(hco_extension)

                    ### HCO Name
                    hco_name_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:name/text()"

                    hco_name =';'.join(tree.xpath(hco_name_path, namespaces=ns))

                    print(hco_name)

                    ### HCO telecom use
                    hco_telecom_use_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:telecom/@use"

                    hco_telecom_use =';'.join(tree.xpath(hco_telecom_use_path, namespaces=ns))

                    print(hco_telecom_use)

                    ### HCO Telecom value
                    hco_telecom_value_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:telecom/@value"

                    hco_telecom_value =';'.join(tree.xpath(hco_telecom_value_path, namespaces=ns))

                    print(hco_telecom_value)

                    ### hco street
                    hco_street_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:addr/n:streetAddressLine/text()"

                    hco_street =';'.join(tree.xpath(hco_street_path, namespaces=ns))

                    print(hco_street)

                    ### hco city
                    hco_city_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:addr/n:city/text()"

                    hco_city =';'.join(tree.xpath(hco_city_path, namespaces=ns))

                    print(hco_city)

                    ### hco state
                    hco_state_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:addr/n:state/text()"

                    hco_state =';'.join(tree.xpath(hco_state_path, namespaces=ns))

                    print(hco_state)

                    ### hco zip
                    hco_zip_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:addr/n:postalCode/text()"

                    hco_zip =';'.join(tree.xpath(hco_zip_path, namespaces=ns))

                    print(hco_zip)

                    ### hco county
                    hco_county_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:addr/n:county/text()"

                    hco_county =';'.join(tree.xpath(hco_county_path, namespaces=ns))

                    print(hco_county)

                    ### hco country
                    hco_country_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:serviceProviderOrganization/n:addr/n:country/text()"

                    hco_country =';'.join(tree.xpath(hco_country_path, namespaces=ns))

                    print(hco_country)

                    ## Facility root
                    facility_root_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:id/@root"

                    facility_root =';'.join(tree.xpath(facility_root_path, namespaces=ns))

                    print(facility_root)

                    ## facility extension
                    facility_extension_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:id/@extension"

                    facility_extension =';'.join(tree.xpath(facility_extension_path, namespaces=ns))

                    print(facility_extension)

                    ## facility name
                    facility_name_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:location/n:name/text()"

                    facility_name =';'.join(tree.xpath(facility_name_path, namespaces=ns))

                    print(facility_name)

                    ## facility street
                    facility_street_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:location/n:addr/n:streetAddressLine/text()"

                    facility_street =';'.join(tree.xpath(facility_street_path, namespaces=ns))

                    print(facility_street)

                    ## facility city
                    facility_city_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:location/n:addr/n:city/text()"

                    facility_city =';'.join(tree.xpath(facility_city_path, namespaces=ns))

                    print(facility_city)

                    ## facility state
                    facility_state_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:location/n:addr/n:state/text()"

                    facility_state =';'.join(tree.xpath(facility_state_path, namespaces=ns))

                    print(facility_state)

                    ## facility zip
                    facility_zip_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:location/n:addr/n:postalCode/text()"

                    facility_zip =';'.join(tree.xpath(facility_zip_path, namespaces=ns))

                    print(facility_zip)

                    ## facility county
                    facility_county_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:location/n:addr/n:county/text()"

                    facility_county =';'.join(tree.xpath(facility_county_path, namespaces=ns))

                    print(facility_county)

                    ## facility country
                    facility_country_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:location/n:healthCareFacility/n:location/n:addr/n:country/text()"

                    facility_country =';'.join(tree.xpath(facility_country_path, namespaces=ns))

                    print(facility_country)

                    ## provider given name
                    provider_given_name_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:assignedPerson/n:name/n:given/text()"

                    provider_given_name =';'.join(tree.xpath(provider_given_name_path, namespaces = ns))

                    print(provider_given_name)

                    ## provider family name
                    provider_family_name_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:assignedPerson/n:name/n:family/text()"

                    provider_family_name =';'.join(tree.xpath(provider_family_name_path, namespaces=ns))

                    print(provider_family_name)

                    ## provider root
                    provider_root_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:id/@root"

                    provider_root =';'.join(tree.xpath(provider_root_path, namespaces=ns))

                    print(provider_root)

                    ## provider extension
                    provider_extension_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:id/@extension"

                    provider_extension =';'.join(tree.xpath(provider_extension_path, namespaces=ns))

                    print(provider_extension)

                    ## provider telecom use
                    provider_telecom_use_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:telecom/@use"

                    provider_telecom_use =';'.join(tree.xpath(provider_telecom_use_path, namespaces=ns))

                    print(provider_telecom_use)

                    ## provider telecom value
                    provider_telecom_value_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:telecom/@value"

                    provider_telecom_value =';'.join(tree.xpath(provider_telecom_value_path, namespaces=ns))

                    print(provider_telecom_value)

                    ## provider street address
                    provider_street_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:addr/n:streetAddressLine/text()"

                    provider_street =';'.join(tree.xpath(provider_street_path, namespaces=ns))

                    print(provider_street)

                    ## provider city
                    provider_city_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:addr/n:city/text()"

                    provider_city =';'.join(tree.xpath(provider_city_path, namespaces=ns))

                    print(provider_city)

                    ## provider state
                    provider_state_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:addr/n:state/text()"

                    provider_state =';'.join(tree.xpath(provider_state_path, namespaces=ns))

                    print(provider_state)

                    ## provider zip
                    provider_zip_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:addr/n:postalCode/text()"

                    provider_zip =';'.join(tree.xpath(provider_zip_path, namespaces=ns))

                    print(provider_zip)

                    ## provider county
                    provider_county_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:addr/n:county/text()"

                    provider_county =';'.join(tree.xpath(provider_county_path, namespaces=ns))

                    print(provider_county)

                    ## provider_country
                    provider_country_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:responsibleParty/n:assignedEntity/n:addr/n:country/text()"

                    provider_country =';'.join(tree.xpath(provider_country_path, namespaces=ns))

                    print(provider_country)

                    ## software
                    software_path = "/n:ClinicalDocument/n:author/n:assignedAuthor/n:assignedAuthoringDevice/n:manufacturerModelName/text()"

                    software =';'.join(tree.xpath(software_path, namespaces=ns))

                    if software == []:
                        software_path = "/n:ClinicalDocument/n:author/n:assignedAuthor/n:assignedAuthoringDevice/n:manufacturerModelName/@displayName"

                        software =';'.join(tree.xpath(software_path, namespaces=ns))

                    print(software)

                    ## software version
                    software_version_path = "/n:ClinicalDocument/n:author/n:assignedAuthor/n:assignedAuthoringDevice/n:softwareName/text()"

                    software_version =';'.join(tree.xpath(software_version_path, namespaces=ns))

                    if software_version == []:
                        software_version_path = "/n:ClinicalDocument/n:author/n:assignedAuthor/n:assignedAuthoringDevice/n:softwareName/@displayName"

                        software_version =';'.join(tree.xpath(software_version_path, namespaces=ns))

                    print(software_version)

                    ## encompassing encounter
                    encompassing_encounter_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:code/n:originalText/text()"

                    encompassing_encounter =';'.join(tree.xpath(encompassing_encounter_path, namespaces=ns))

                    print(encompassing_encounter)

                    ## encompassing encounter code
                    encompassing_encounter_code_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:code/@code"
                    encompassing_encounter_code_system_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:code/@codeSystem"
                    encompassing_encounter_name_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:code/@displayName"

                    encompassing_encounter_code =';'.join(tree.xpath(encompassing_encounter_code_path, namespaces=ns))
                    encompassing_encounter_code_system =';'.join(tree.xpath(encompassing_encounter_code_path, namespaces=ns))
                    encompassing_encounter_name =';'.join(tree.xpath(encompassing_encounter_name_path, namespaces=ns))

                    print(encompassing_encounter_code)

                    ## discharge disposition
                    discharge_disposition_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:encounter/sdtc:dischargeDispositionCode/text()"

                    discharge_disposition =';'.join(tree.xpath(discharge_disposition_path, namespaces=ns))

                    print(discharge_disposition)

                    ## encounter time
                    encounter_time_path = "/n:ClinicalDocument/n:componentOf/n:encompassingEncounter/n:effectiveTime/n:low/@value"

                    encounter_time =';'.join(tree.xpath(encounter_time_path, namespaces=ns))

                    print(encounter_time)

                    ## Miscellaneous Notes
                    misc_notes_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section[n:templateId/@root='1.3.6.1.4.1.19376.1.5.3.1.3.4']/n:text"

                    misc_notes = len(tree.xpath(misc_notes_path, namespaces=ns))

                    print(misc_notes)

                    ## medications aborted
                    abort_med_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:substanceAdministration/@moodCode"

                    abort_med =';'.join(tree.xpath(abort_med_path, namespaces=ns))

                    print(abort_med)

                    pregSupEffectiveTimeLow_path = "/n:ClinicalDocument/n:component/n:structuredBody/n:component/n:section/n:entry/n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.293']/n:effectiveTime/n:low/@value"
                    pregSupTimeLow =';'.join(tree.xpath(pregSupEffectiveTimeLow_path, namespaces = ns))
                    print(pregSupTimeLow)

                    pregSupTimeHigh_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.293']/n:effectiveTime/n:high/@value"
                    pregSupTimeHigh =';'.join(tree.xpath(pregSupTimeHigh_path, namespaces=ns))
                    print(pregSupTimeHigh)

                    pregSupDetMethodCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.293']/n:methodCode/@code"
                    pregSupDetMethodCode =';'.join(tree.xpath(pregSupDetMethodCode_path, namespaces=ns))
                    print(pregSupDetMethodCode)

                    pregSupDetMethodCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.293']/n:methodCode/@codeSystem"
                    pregSupDetMethodCodeSystem =';'.join(tree.xpath(pregSupDetMethodCodeSystem_path, namespaces=ns))
                    print(pregSupDetMethodCodeSystem)

                    pregSupDetMethodDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.293']/n:methodCode/@displayName"
                    pregSupDetMethodDisplay =';'.join(tree.xpath(pregSupDetMethodDisplay_path, namespaces=ns))
                    print(pregSupDetMethodDisplay)

                    pregSupRecordDate_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.293']/n:author/n:time/@value"
                    pregSupRecordDate =';'.join(tree.xpath(pregSupRecordDate_path, namespaces=ns))
                    print(pregSupRecordDate)

                    pregSupEstDelivDate_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.297']/n:value/@value"
                    pregSupEstDelivDate =';'.join(tree.xpath(pregSupEstDelivDate_path, namespaces=ns))
                    print(pregSupEstDelivDate)

                    pregSupDelivDateMethodCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.297']/n:code/@code"
                    pregSupDelivDateMethodCode =';'.join(tree.xpath(pregSupDelivDateMethodCode_path, namespaces=ns))
                    print(pregSupDelivDateMethodCode)

                    pregSupDelivDateMethodCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.297']/n:code/@codeSystem"
                    pregSupDelivDateMethodCodeSystem =';'.join(tree.xpath(pregSupDelivDateMethodCodeSystem_path, namespaces=ns))
                    print(pregSupDelivDateMethodCodeSystem)

                    pregSupDelivDateMethodDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.297']/n:code/@displayName"
                    pregSupDelivDateMethodDisplay =';'.join(tree.xpath(pregSupDelivDateMethodDisplay_path, namespaces=ns))
                    print(pregSupDelivDateMethodDisplay)

                    patGenderIdentityCode_path = "//n:observation[n:templateId[@root='2.16.840.1.113883.10.20.34.3.45']]/n:value/@code"
                    patGenderIdentityCode =';'.join(tree.xpath(patGenderIdentityCode_path, namespaces=ns))
                    print(patGenderIdentityCode)

                    patGenderIdentityCodeSystem_path = "//n:observation[n:templateId[@root='2.16.840.1.113883.10.20.34.3.45']]/n:value/@codeSystem"
                    patGenderIdentityCodeSystem =';'.join(tree.xpath(patGenderIdentityCodeSystem_path, namespaces=ns))
                    print(patGenderIdentityCodeSystem)

                    patGenderIdentityCode_path = "//n:observation[n:templateId[@root='2.16.840.1.113883.10.20.34.3.45']]/n:value/@displayName"
                    patGenderIdentityCode =';'.join(tree.xpath(patGenderIdentityCode_path, namespaces=ns))
                    print(patGenderIdentityCode)

                    pregSupLastMenst_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.30.3.34']/n:value/@value"
                    pregSupLastMenst =';'.join(tree.xpath(pregSupLastMenst_path, namespaces=ns))
                    print(pregSupLastMenst)

                    pregSupOutcomeCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.284']/n:value/@code"
                    pregSupOutcomeCode =';'.join(tree.xpath(pregSupOutcomeCode_path, namespaces=ns))
                    print(pregSupOutcomeCode)

                    pregSupOutcomeCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.284']/n:value/@codeSystem"
                    pregSupOutcomeCodeSystem =';'.join(tree.xpath(pregSupOutcomeCodeSystem_path, namespaces=ns))
                    print(pregSupOutcomeCodeSystem)

                    pregSupOutcomeDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.284']/n:value/@displayName"
                    pregSupOutcomeDisplay =';'.join(tree.xpath(pregSupOutcomeDisplay_path, namespaces=ns))
                    print(pregSupOutcomeDisplay)

                    pregSupOutcomeTime_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.284']/n:effectiveTime/@value"
                    pregSupOutcomeTime =';'.join(tree.xpath(pregSupOutcomeTime_path, namespaces=ns))
                    print(pregSupOutcomeTime)

                    PregSupPostPartStatusCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.285']/n:value/@code"
                    PregSupPostPartStatusCode =';'.join(tree.xpath(PregSupPostPartStatusCode_path, namespaces=ns))
                    print(PregSupPostPartStatusCode)

                    PregSupPostPartStatusCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.285']/n:value/@codeSystem"
                    PregSupPostPartStatusCodeSystem =';'.join(tree.xpath(PregSupPostPartStatusCodeSystem_path, namespaces=ns))
                    print(PregSupPostPartStatusCodeSystem)

                    PregSupPostPartStatusDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.285']/n:value/@displayName"
                    PregSupPostPartStatusDisplay =';'.join(tree.xpath(PregSupPostPartStatusDisplay_path, namespaces=ns))
                    print(PregSupPostPartStatusDisplay)

                    resultOrgTriggerCode_path = "//n:organizer[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.35']/n:code/@code"
                    resultOrgTriggerCode =';'.join(tree.xpath(resultOrgTriggerCode_path, namespaces = ns))
                    print(resultOrgTriggerCode)

                    resultOrgTriggerCodeSystem_path = "//n:organizer[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.35']/n:code/@codeSystem"
                    resultOrgTriggerCodeSystem =';'.join(tree.xpath(resultOrgTriggerCodeSystem_path, namespaces=ns))
                    print(resultOrgTriggerCodeSystem)

                    resultOrgTriggerDisplay_path = "//n:organizer[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.35']/n:code/@displayName"
                    resultOrgTriggerDisplay =';'.join(tree.xpath(resultOrgTriggerDisplay_path, namespaces=ns))
                    print(resultOrgTriggerDisplay)

                    medAdminTriggerCode_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@code"
                    medAdminTriggerCode =';'.join(tree.xpath(medAdminTriggerCode_path, namespaces=ns))
                    print(medAdminTriggerCode)

                    medAdminTriggerCodeSystem_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@codeSystem"
                    medAdminTriggerCodeSystem =';'.join(tree.xpath(medAdminTriggerCodeSystem_path, namespaces=ns))
                    print(medAdminTriggerCodeSystem)

                    medAdminTriggerDisplay_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@displayName"
                    medAdminTriggerDisplay =';'.join(tree.xpath(medAdminTriggerDisplay_path, namespaces=ns))
                    print(medAdminTriggerDisplay)

                    medPlannedCode_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.22.4.23']/n:manufacturedMaterial/n:code/@code"
                    medPlannedCode =';'.join(tree.xpath(medPlannedCode_path, namespaces=ns))
                    print(medPlannedCode)

                    medPlannedCodeSystem_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.22.4.23']/n:manufacturedMaterial/n:code/@codeSystem"
                    medPlannedCodeSystem =';'.join(tree.xpath(medPlannedCodeSystem_path, namespaces = ns))
                    print(medPlannedCodeSystem)

                    medPlannedDisplay_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.22.4.23']/n:manufacturedMaterial/n:code/@displayName"
                    medPlannedDisplay =';'.join(tree.xpath(medPlannedDisplay_path, namespaces=ns))
                    print(medPlannedDisplay)

                    medPlannedTriggerCode_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@code"
                    medPlannedTriggerCode =';'.join(tree.xpath(medPlannedTriggerCode_path, namespaces=ns))

                    medPlannedTriggerCodeSystem_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@codeSystem"
                    medPlannedTriggerCodeSystem =';'.join(tree.xpath(medPlannedTriggerCodeSystem_path, namespaces=ns))
                    print(medPlannedTriggerCodeSystem)
                    
                    medPlannedTriggerDisplay_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@displayName"
                    medPlannedTriggerDisplay =';'.join(tree.xpath(medPlannedTriggerDisplay_path, namespaces=ns))
                    print(medPlannedTriggerDisplay)

                    medCodeCode_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.22.4.23']/n:manufacturedMaterial/n:code/@code"
                    medCodeCode =';'.join(tree.xpath(medCodeCode_path, namespaces=ns))
                    print(medCodeCode)

                    medCodeCodeSystem_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.22.4.23']/n:manufacturedMaterial/n:code/@codeSystem"
                    medCodeCodeSystem =';'.join(tree.xpath(medCodeCodeSystem_path, namespaces=ns))
                    print(medCodeCodeSystem)

                    medCodeDisplay_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.22.4.23']/n:manufacturedMaterial/n:code/@displayName"
                    medCodeDisplay =';'.join(tree.xpath(medCodeDisplay_path, namespaces = ns))
                    print(medCodeDisplay)

                    medTriggerCode_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@code"
                    medTriggerCode =';'.join(tree.xpath(medTriggerCode_path, namespaces=ns))
                    print(medTriggerCode)

                    medTriggerCodeSystem_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@codeSystem"
                    medTriggerCodeSystem =';'.join(tree.xpath(medTriggerCodeSystem_path, namespaces=ns))
                    print(medTriggerCodeSystem)

                    medTriggerDisplay_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.36']/n:manufacturedMaterial/n:code/@displayName"
                    medTriggerDisplay =';'.join(tree.xpath(medTriggerDisplay_path, namespaces=ns))
                    print(medTriggerDisplay)

                    immuVaccTrigCode_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.38']/n:manufacturedMaterial/n:code/@code"
                    immuVaccTrigCode =';'.join(tree.xpath(immuVaccTrigCode_path, namespaces=ns))
                    print(immuVaccTrigCode)

                    immuVaccTrigCodeSystem_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.38']/n:manufacturedMaterial/n:code/@codeSystem"
                    immuVaccTrigCodeSystem =';'.join(tree.xpath(immuVaccTrigCodeSystem_path, namespaces=ns))
                    print(immuVaccTrigCodeSystem)

                    immuVaccTrigDisplay_path = "//n:manufacturedProduct[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.38']/n:manufacturedMaterial/n:code/@displayName"
                    immuVaccTrigDisplay =';'.join(tree.xpath(immuVaccTrigDisplay_path, namespaces=ns))
                    print(immuVaccTrigDisplay)

                    travelPurpCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.51']/n:code/@code"
                    travelPurpCode =';'.join(tree.xpath(travelPurpCode_path, namespaces=ns))
                    print(travelPurpCode)

                    travelPurpCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.51']/n:code/@codeSystem"
                    travelPurpCodeSystem =';'.join(tree.xpath(travelPurpCodeSystem_path, namespaces=ns))
                    print(travelPurpCodeSystem)

                    travelPurpDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.51']/n:code/@displayName"
                    travelPurpDisplay =';'.join(tree.xpath(travelPurpDisplay_path, namespaces = ns))
                    print(travelPurpDisplay)

                    travelTypeCode_path = "//n:organizer[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.50']/n:code/@code"
                    travelTypeCode =';'.join(tree.xpath(travelTypeCode_path, namespaces=ns))
                    print(travelTypeCode)

                    travelTypeCodeSystem_path = "//n:organizer[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.50']/n:code/@codeSystem"
                    travelTypeCodeSystem =';'.join(tree.xpath(travelTypeCodeSystem_path, namespaces=ns))
                    print(travelTypeCodeSystem)
                    
                    travelTypeDisplay_path = "//n:organizer[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.50']/n:code/@displayName"
                    travelTypeDisplay =';'.join(tree.xpath(travelTypeDisplay_path, namespaces=ns))
                    print(travelTypeDisplay)

                    travelTransDetailCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.49']/n:code/@code"
                    travelTransDetailCode =';'.join(tree.xpath(travelTransDetailCode_path, namespaces=ns))
                    print(travelTransDetailCode)

                    travelTransDetailCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.49']/n:code/@codeSystem"
                    travelTransDetailCodeSystem =';'.join(tree.xpath(travelTransDetailCodeSystem_path, namespaces=ns))
                    print(travelTransDetailCodeSystem)

                    travelTransDetailDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.49']/n:code/@displayName"
                    travelTransDetailDisplay =';'.join(tree.xpath(travelTransDetailDisplay_path, namespaces=ns))
                    print(travelTransDetailDisplay)

                    travelTransDetailValue_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.49']/n:value/@value"
                    travelTransDetailValue =';'.join(tree.xpath(travelTransDetailValue_path, namespaces=ns))
                    print(travelTransDetailValue)
                    
                    occupationCurrentCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:value/@code"
                    occupationCurrentCode =';'.join(tree.xpath(occupationCurrentCode_path, namespaces=ns))
                    print(occupationCurrentCode)

                    occupationCurrentCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:value/@codeSystem"
                    occupationCurrentCodeSystem =';'.join(tree.xpath(occupationCurrentCodeSystem_path, namespaces=ns))
                    print(occupationCurrentCodeSystem)

                    occupationCurrentDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:value/@displayName"
                    occupationCurrentDisplay =';'.join(tree.xpath(occupationCurrentDisplay_path, namespaces=ns))
                    print(occupationCurrentDisplay)

                    occupationUsualCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.221']/n:value"
                    occupationUsualCode =';'.join(tree.xpath(occupationUsualCode_path, namespaces = ns))
                    print(occupationUsualCode)

                    occupationUsualCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.221']/n:value/@codeSystem"
                    occupationUsualCodeSystem =';'.join(tree.xpath(occupationUsualCodeSystem_path, namespaces=ns))
                    print(occupationUsualCodeSystem)
                    
                    occupationUsualDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.221']/n:value/@displayName"
                    occupationUsualDisplay =';'.join(tree.xpath(occupationUsualDisplay_path, namespaces=ns))
                    print(occupationUsualDisplay)
                    
                    industryCurrentCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.216']/n:value/@code"
                    industryCurrentCode =';'.join(tree.xpath(industryCurrentCode_path, namespaces=ns))
                    print(industryCurrentCode)

                    industryCurrentCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.216']/n:value/@codeSystem"
                    industryCurrentCodeSystem =';'.join(tree.xpath(industryCurrentCodeSystem_path, namespaces=ns))
                    print(industryCurrentCodeSystem)

                    industryCurrentDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.216']/n:value/@DisplayName"
                    industryCurrentDisplay =';'.join(tree.xpath(industryCurrentDisplay_path, namespaces=ns))
                    print(industryCurrentDisplay)

                    industryUsualCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.219']/n:value/@code"
                    industryUsualCode =';'.join(tree.xpath(industryUsualCode_path, namespaces=ns))
                    print(industryUsualCode)

                    industryUsualCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.219']/n:value/@codeSystem"
                    industryUsualCodeSystem =';'.join(tree.xpath(industryUsualCodeSystem_path, namespaces=ns))
                    print(industryUsualCodeSystem)

                    industryUsualDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.219']/n:value/@displayName"
                    industryUsualDisplay =';'.join(tree.xpath(industryUsualDisplay_path, namespaces=ns))
                    print(industryUsualDisplay)

                    currentEmployerName_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:name/text()"
                    currentEmployerName =';'.join(tree.xpath(currentEmployerName_path, namespaces=ns))
                    print(currentEmployerName)

                    currentEmployerPhone_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:telecom/@value"
                    currentEmployerPhone =';'.join(tree.xpath(currentEmployerPhone_path, namespaces=ns))
                    print(currentEmployerPhone)

                    currentEmployerAddressStreet_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:addr/n:streetAddressLine/text()"
                    currentEmployerAddressStreet =';'.join(tree.xpath(currentEmployerAddressStreet_path, namespaces=ns))
                    print(currentEmployerAddressStreet)

                    currentEmployerAddressCounty_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:addr/n:county/text()"
                    currentEmployerAddressCounty =';'.join(tree.xpath(currentEmployerAddressCounty_path, namespaces=ns))
                    print(currentEmployerAddressCounty)

                    currentEmployerAddressCity_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:addr/n:city/text()"
                    currentEmployerAddressCity =';'.join(tree.xpath(currentEmployerAddressCity_path, namespaces=ns))
                    print(currentEmployerAddressCity)

                    currentEmployerAddressState_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:state/text()"
                    currentEmployerAddressState =';'.join(tree.xpath(currentEmployerAddressState_path, namespaces=ns))
                    print(currentEmployerAddressState)

                    currentEmployerAddressZip_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:addr/n:postalCode/text()"
                    currentEmployerAddressZip =';'.join(tree.xpath(currentEmployerAddressZip_path, namespaces=ns))
                    print(currentEmployerAddressZip)

                    currentEmployerAddressCountry_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.217' and statusCode/@code='active' and not(effectiveTime/high)]/n:participant/n:participantRole/n:playingEntity/n:addrcountry/text()"
                    currentEmployerAddressCountry =';'.join(tree.xpath(currentEmployerAddressCountry_path, namespaces=ns))
                    print(currentEmployerAddressCountry)

                    ocupationExposure_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.215']/n:value/@text()"
                    ocupationExposure =';'.join(tree.xpath(ocupationExposure_path, namespaces=ns))
                    print(ocupationExposure)

                    EmploymentStatusCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.212']/n:value/@code"
                    EmploymentStatusCode =';'.join(tree.xpath(EmploymentStatusCode_path, namespaces=ns))
                    print(EmploymentStatusCode)

                    EmploymentStatusCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.212']/n:value/@codeSystem"
                    EmploymentStatusCodeSystem =';'.join(tree.xpath(EmploymentStatusCodeSystem_path, namespaces=ns))
                    print(EmploymentStatusCodeSystem)

                    EmploymentStatusDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.212']/n:value/@displayName"
                    EmploymentStatusDisplay =';'.join(tree.xpath(EmploymentStatusDisplay_path, namespaces=ns))
                    print(EmploymentStatusDisplay)

                    pregSupEstGestAge_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.280']/n:value/@value"
                    pregSupEstGestAge =';'.join(tree.xpath(pregSupEstGestAge_path, namespaces=ns))
                    print(pregSupEstGestAge)

                    pregSupEstGestAgeDate_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.280']/n:effectiveTime/@value"
                    pregSupEstGestAgeDate =';'.join(tree.xpath(pregSupEstGestAgeDate_path, namespaces=ns))
                    print(pregSupEstGestAgeDate)

                    pregSupEstGestAgeMethodCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.280']/n:code/@code"
                    pregSupEstGestAgeMethodCode =';'.join(tree.xpath(pregSupEstGestAgeMethodCode_path, namespaces=ns))
                    print(pregSupEstGestAgeMethodCode)

                    pregSupEstGestAgeMethodCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.280']/n:code/@codeSystem"
                    pregSupEstGestAgeMethodCodeSystem =';'.join(tree.xpath(pregSupEstGestAgeMethodCodeSystem_path, namespaces=ns))
                    print(pregSupEstGestAgeMethodCodeSystem)

                    pregSupEstGestAgeMethodDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.280']/n:code/@displayName"
                    pregSupEstGestAgeMethodDisplay =';'.join(tree.xpath(pregSupEstGestAgeMethodDisplay_path, namespaces=ns))
                    print(pregSupEstGestAgeMethodDisplay)

                    medHistCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.4']/n:value/@code"
                    medHistCode =';'.join(tree.xpath(medHistCode_path, namespaces=ns))
                    print(medHistCode)

                    medHistCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.4']/n:value/@codeSystem"
                    medHistCodeSystem =';'.join(tree.xpath(medHistCodeSystem_path, namespaces=ns))
                    print(medHistCodeSystem)

                    medHistDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.4']/n:value/@displayName"
                    medHistDisplay =';'.join(tree.xpath(medHistDisplay_path, namespaces=ns))
                    print(medHistDisplay)

                    medHistText_path = "//n:section[n:templateId/@root='2.16.840.1.113883.10.20.22.2.20']/n:text"
                    medHistText =';'.join(tree.xpath(medHistText_path, namespaces=ns))
                    print(medHistText)

                    systemsReviewText_path = "//n:section[n:templateId/@root='2.16.840.1.113883.10.20.22.2.18']/n:text"
                    systemsReviewText =';'.join(tree.xpath(systemsReviewText_path, namespaces=ns))
                    print(systemsReviewText)

                    specimenSourceCode_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.415']/n:targetSiteCode/@code"
                    specimenSourceCode =';'.join(tree.xpath(specimenSourceCode_path, namespaces=ns))
                    print(specimenSourceCode)

                    specimenSourceCodeSystem_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.415']/n:targetSiteCode/@codeSystem"
                    specimenSourceCodeSystem =';'.join(tree.xpath(specimenSourceCodeSystem_path, namespaces=ns))
                    print(specimenSourceCodeSystem)

                    specimenSourceDisplay_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.415']/n:targetSiteCode/@displayName"
                    specimenSourceDisplay =';'.join(tree.xpath(specimenSourceDisplay_path, namespaces=ns))
                    print(specimenSourceDisplay)

                    specimenTypeCode_path = "//n:participant[n:templateId/@root='2.16.840.1.113883.10.20.22.4.410']/n:participantRole/n:code/@code"
                    specimenTypeCode =';'.join(tree.xpath(specimenTypeCode_path, namespaces=ns))
                    print(specimenTypeCode)

                    specimenId_path = "//n:participant[n:templateId/@root='2.16.840.1.113883.10.20.22.4.410']/n:participantRole/n:id/@value"
                    specimenId =';'.join(tree.xpath(specimenId_path, namespaces=ns))
                    print(specimenId)

                    specimentCollectDate_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.415']/n:effectiveTime/n:low/@value"
                    specimentCollectDate =';'.join(tree.xpath(specimentCollectDate_path, namespaces=ns))
                    print(specimentCollectDate)

                    vitalsValue_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.27']/n:value/@value"
                    vitalsValue =';'.join(tree.xpath(vitalsValue_path, namespaces=ns))
                    print(vitalsValue)

                    vitalsUnit_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.27']/n:value/@unit"
                    vitalsUnit =';'.join(tree.xpath(vitalsUnit_path, namespaces=ns))
                    print(vitalsUnit)

                    medTherRespValueCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.37']/n:value/@code"
                    medTherRespValueCode =';'.join(tree.xpath(medTherRespValueCode_path, namespaces=ns))
                    print(medTherRespValueCode)

                    medTherRespValueCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.37']/n:value/@codeSystem"
                    medTherRespValueCodeSystem =';'.join(tree.xpath(medTherRespValueCodeSystem_path, namespaces=ns))
                    print(medTherRespValueCodeSystem)

                    medTherRespValueDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.37']/n:value/@displayName"
                    medTherRespValueDisplay =';'.join(tree.xpath(medTherRespValueDisplay_path, namespaces=ns))
                    print(medTherRespValueDisplay)
                    
                    homelessFlag_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.109']/n:value='105526001'"
                    homelessFlag =str(tree.xpath(homelessFlag_path, namespaces=ns))
                    print(homelessFlag)

                    procActCode_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.22.4.12']/n:code/@code"
                    procActCode =';'.join(tree.xpath(procActCode_path, namespaces=ns))
                    print(procActCode)

                    procActCodeSystem_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.22.4.12']/n:code/@codeSystem"
                    procActCodeSystem =';'.join(tree.xpath(procActCodeSystem_path, namespaces=ns))
                    print(procActCodeSystem)

                    procActCodeDisplay_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.22.4.12']/n:code/@displayName"
                    procActCodeDisplay =';'.join(tree.xpath(procActCodeDisplay_path, namespaces=ns))
                    print(procActCodeDisplay)

                    procObsCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.13']/n:code/@code"
                    procObsCode =';'.join(tree.xpath(procObsCode_path, namespaces=ns))
                    print(procObsCode)

                    procObsCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.13']/n:code/@codeSystem"
                    procObsCodeSystem =';'.join(tree.xpath(procObsCodeSystem_path, namespaces=ns))
                    print(procObsCodeSystem)

                    procObsDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.13']/n:code/@displayName"
                    procObsDisplay =';'.join(tree.xpath(procObsDisplay_path, namespaces=ns))
                    print(procObsDisplay)

                    procCode_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.14']/n:code/@code"
                    procCode =';'.join(tree.xpath(procCode_path, namespaces=ns))
                    print(procCode)

                    procCodeSystem_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.14']/n:code/@codeSystem"
                    procCodeSystem =';'.join(tree.xpath(procCodeSystem_path, namespaces=ns))
                    print(procCodeSystem)
                    
                    procDisplay_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.14']/n:code/@displayName"
                    procDisplay =';'.join(tree.xpath(procDisplay_path, namespaces=ns))
                    print(procDisplay)

                    procTriggerActCode_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.45']/n:code/@code"
                    procTriggerActCode =';'.join(tree.xpath(procTriggerActCode_path, namespaces=ns))
                    print(procTriggerActCode)

                    procTriggerActCodeSystem_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.45']/n:code/@codeSystem"
                    procTriggerActCodeSystem =';'.join(tree.xpath(procTriggerActCodeSystem_path, namespaces=ns))
                    print(procTriggerActCodeSystem)

                    procTriggerActDisplay_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.45']/n:code/@displayName"
                    procTriggerActDisplay =';'.join(tree.xpath(procTriggerActDisplay_path, namespaces=ns))
                    print(procTriggerActDisplay)

                    procTriggerObsCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.46']/n:code/@code"
                    procTriggerObsCode =';'.join(tree.xpath(procTriggerObsCode_path, namespaces=ns))
                    print(procTriggerObsCode)
                    
                    procTriggerObsCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.46']/n:code/@codeSystem"
                    procTriggerObsCodeSystem =';'.join(tree.xpath(procTriggerObsCodeSystem_path, namespaces=ns))
                    print(procTriggerObsCodeSystem)

                    procTriggerObsDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.46']/n:code/@displayName"
                    procTriggerObsDisplay =';'.join(tree.xpath(procTriggerObsDisplay_path, namespaces=ns))
                    print(procTriggerObsDisplay)

                    procTriggerProcCode_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.44']/n:code/@code"
                    procTriggerProcCode =';'.join(tree.xpath(procTriggerProcCode_path, namespaces=ns))
                    print(procTriggerProcCode)

                    procTriggerProcCodeSystem_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.44']/n:code/@codeSystem"
                    procTriggerProcCodeSystem =';'.join(tree.xpath(procTriggerProcCodeSystem_path, namespaces=ns))
                    print(procTriggerProcCodeSystem)

                    procTriggerProcDisplay_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.44']/n:code/@displayName"
                    procTriggerProcDisplay =';'.join(tree.xpath(procTriggerProcDisplay_path, namespaces=ns))
                    print(procTriggerProcDisplay)

                    procPlannedActCode_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.22.4.39']/n:code/@code"
                    procPlannedActCode =';'.join(tree.xpath(procPlannedActCode_path, namespaces=ns))
                    print(procPlannedActCode)

                    procPlannedActCodeSystem_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.22.4.39']/n:code/@codeSystem"
                    procPlannedActCodeSystem =';'.join(tree.xpath(procPlannedActCodeSystem_path, namespaces=ns))
                    print(procPlannedActCodeSystem)

                    procPlannedActDisplay_path = "//n:act[n:templateId/@root='2.16.840.1.113883.10.20.22.4.39']/n:code/@displayName"
                    procPlannedActDisplay =';'.join(tree.xpath(procPlannedActDisplay_path, namespaces=ns))
                    print(procPlannedActDisplay)

                    procPlannedObsCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.44']/n:code/@code"
                    procPlannedObsCode =';'.join(tree.xpath(procPlannedObsCode_path, namespaces=ns))
                    print(procPlannedObsCode)
                    
                    procPlannedObsCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.44']/n:code/@codeSystem"
                    procPlannedObsCodeSystem =';'.join(tree.xpath(procPlannedObsCodeSystem_path, namespaces=ns))
                    print(procPlannedObsCodeSystem)

                    procPlannedObsDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.22.4.44']/n:code/@displayName"
                    procPlannedObsDisplay =';'.join(tree.xpath(procPlannedObsDisplay_path, namespaces=ns))
                    print(procPlannedObsDisplay)

                    
                    procPlannedProcCode_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.41']/n:code/@code"
                    procPlannedProcCode =';'.join(tree.xpath(procPlannedProcCode_path, namespaces=ns))
                    print(procPlannedProcCode)

                    procPlannedProcCodeSystem_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.41']/n:code/@codeSystem"
                    procPlannedProcCodeSystem =';'.join(tree.xpath(procPlannedProcCodeSystem_path, namespaces=ns))
                    print(procPlannedProcCodeSystem)

                    procPlannedProcDisplay_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.22.4.41']/n:code/@displayName"
                    procPlannedProcDisplay =';'.join(tree.xpath(procPlannedProcDisplay_path, namespaces=ns))
                    print(procPlannedProcDisplay)
                        

                    procPlannedTrigObsCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.43']/n:code/@code"
                    procPlannedTrigObsCode =';'.join(tree.xpath(procPlannedTrigObsCode_path, namespaces=ns))
                    print(procPlannedTrigObsCode)

                    procPlannedTrigObsCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.43']/n:code/@codeSystem"
                    procPlannedTrigObsCodeSystem =';'.join(tree.xpath(procPlannedTrigObsCodeSystem_path, namespaces=ns))
                    print(procPlannedTrigObsCodeSystem)

                    procPlannedTrigObsDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.43']/n:code/@displayName"
                    procPlannedTrigObsDisplay =';'.join(tree.xpath(procPlannedTrigObsDisplay_path, namespaces=ns))
                    print(procPlannedTrigObsDisplay)

                    procPlannedTriggerProcCode_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.42']/n:code/@code"
                    procPlannedTriggerProcCode =';'.join(tree.xpath(procPlannedTriggerProcCode_path, namespaces=ns))
                    print(procPlannedTriggerProcCode)

                    procPlannedTriggerProcCodeSystem_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.42']/n:code/@codeSystem"
                    procPlannedTriggerProcCodeSystem =';'.join(tree.xpath(procPlannedTriggerProcCodeSystem_path, namespaces=ns))
                    print(procPlannedTriggerProcCodeSystem)

                    procPlannedTriggerProcDisplay_path = "//n:procedure[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.42']/n:code/@displayName"
                    procPlannedTriggerProcDisplay =';'.join(tree.xpath(procPlannedTriggerProcDisplay_path, namespaces=ns))
                    print(procPlannedTriggerProcDisplay)

                    disabilityStatusCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.47']/n:code/@code"
                    disabilityStatusCode =';'.join(tree.xpath(disabilityStatusCode_path, namespaces=ns))
                    print(disabilityStatusCode)

                    disabilityStatusCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.47']/n:code/@codeSystem"
                    disabilityStatusCodeSystem =';'.join(tree.xpath(disabilityStatusCodeSystem_path, namespaces=ns))
                    print(disabilityStatusCodeSystem)

                    disabilityStatusDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.47']/n:code/@displayName"
                    disabilityStatusDisplay =';'.join(tree.xpath(disabilityStatusDisplay_path, namespaces=ns))
                    print(disabilityStatusDisplay)

                    emergencyOutbreakCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.40']/n:code/@code"
                    emergencyOutbreakCode =';'.join(tree.xpath(emergencyOutbreakCode_path, namespaces=ns))
                    print(emergencyOutbreakCode)

                    emergencyOutbreakCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.40']/n:code/@codeSystem"
                    emergencyOutbreakCodeSystem =';'.join(tree.xpath(emergencyOutbreakCodeSystem_path, namespaces=ns))
                    print(emergencyOutbreakCodeSystem)

                    emergencyOutbreakDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.40']/n:code/@displayName"
                    emergencyOutbreakDisplay =';'.join(tree.xpath(emergencyOutbreakDisplay_path, namespaces=ns))
                    print(emergencyOutbreakDisplay)

                    exposureInfoCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.52']/n:code/@code"
                    exposureInfoCode =';'.join(tree.xpath(exposureInfoCode_path, namespaces=ns))
                    print(exposureInfoCode)

                    exposureInfoCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.52']/n:code/@codeSystem"
                    exposureInfoCodeSystem =';'.join(tree.xpath(exposureInfoCodeSystem_path, namespaces=ns))
                    print(exposureInfoCodeSystem)

                    exposureInfoDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.52']/n:code/@displayName"
                    exposureInfoDisplay =';'.join(tree.xpath(exposureInfoDisplay_path, namespaces=ns))
                    print(exposureInfoDisplay)

                    tribalAffiliationCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.48']/n:code/@code"
                    tribalAffiliationCode =';'.join(tree.xpath(tribalAffiliationCode_path, namespaces=ns))
                    print(tribalAffiliationCode)

                    tribalAffiliationCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.48']/n:code/@codeSystem"
                    tribalAffiliationCodeSystem =';'.join(tree.xpath(tribalAffiliationCodeSystem_path, namespaces=ns))
                    print(tribalAffiliationCodeSystem)

                    tribalAffiliationDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.48']/n:code/@displayName"
                    tribalAffiliationDisplay =';'.join(tree.xpath(tribalAffiliationDisplay_path, namespaces=ns))
                    print(tribalAffiliationDisplay)

                    tribalEnrollment_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.48']/n:value/@value"
                    tribalEnrollment =';'.join(tree.xpath(tribalEnrollment_path, namespaces=ns))
                    print(tribalEnrollment)

                    vaccineCredPatAssertCode_path = "//Nobservation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.55']/n:value/@code"
                    vaccineCredPatAssertCode =';'.join(tree.xpath(vaccineCredPatAssertCode_path, namespaces=ns))
                    print(vaccineCredPatAssertCode)
                    
                    vaccineCredPatAssertCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.55']/n:value/@codeSystem"
                    vaccineCredPatAssertCodeSystem =';'.join(tree.xpath(vaccineCredPatAssertCodeSystem_path, namespaces=ns))
                    print(vaccineCredPatAssertCodeSystem)
                    
                    vaccineCredPatAssertDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.55']/n:value/@displayname"
                    vaccineCredPatAssertDisplay =';'.join(tree.xpath(vaccineCredPatAssertDisplay_path, namespaces=ns))
                    print(vaccineCredPatAssertDisplay)

                    nationalityCountryCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.54']/n:value/@code"
                    nationalityCountryCode =';'.join(tree.xpath(nationalityCountryCode_path, namespaces=ns))
                    print(nationalityCountryCode)

                    nationalityCountryCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.54']/n:value/@codeSystem"
                    nationalityCountryCodeSystem =';'.join(tree.xpath(nationalityCountryCodeSystem_path, namespaces=ns))
                    print(nationalityCountryCodeSystem)

                    nationalityCountryDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.54']/n:value/@displayName"
                    nationalityCountryDisplay =';'.join(tree.xpath(nationalityCountryDisplay_path, namespaces=ns))
                    print(nationalityCountryDisplay)

                    
                    residenceCountryCode_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.53']/n:value/@code"
                    residenceCountryCode =';'.join(tree.xpath(residenceCountryCode_path, namespaces=ns))
                    print(residenceCountryCode)

                    residenceCountryCodeSystem_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.53']/n:value/@codeSystem"
                    residenceCountryCodeSystem =';'.join(tree.xpath(residenceCountryCodeSystem_path, namespaces=ns))
                    print(residenceCountryCodeSystem)

                    residenceCountryDisplay_path = "//n:observation[n:templateId/@root='2.16.840.1.113883.10.20.15.2.3.53']/n:value/@displayName"
                    residenceCountryDisplay =';'.join(tree.xpath(residenceCountryDisplay_path, namespaces=ns))
                    print(residenceCountryDisplay)


                    ## Build out datastructure

                    with open(f"{output_path}\\{year}{month}{day}_zip.csv", mode = 'a', newline='') as file:
                        writer = csv.writer(file) 
                        writer.writerow([doc_oid_root, doc_oid_ext, doc_oid_assigningauthor, set_id_root, set_id_ext, set_id_assigningAuthor,
                            effective_time, vcn, legal_given_names, given_names, legal_family_names, family_names,
                             patient_address_street, patient_address_city, patient_address_state, patient_address_zip, patient_address_county, patient_address_country,
                             patient_telecoms, patient_telecom_uses, patient_dob, patient_race_code, patient_race_code_system, patient_race_name,
                             patient_ethnicity_code, patient_ethnicity_code_system, patient_ethnicity_name, patient_gender_code, patient_gender_code_system, patient_gender_name,
                             patient_marital_code, patient_marital_code_system, patient_marital_name, patient_language_code, patient_pregnant1, patient_pregnant2,
                             patient_deceased, patient_mrn, patient_smoking, patient_tobacco, patient_alcohol, patient_immunization_status,
                             patient_ssn1, patient_ssn2, guardian_presence, guardian_given_names, guardian_family_name, guardian_street,
                             guardian_city, guardian_state, guardian_zip, guardian_county, guardian_country, guardian_telecom_value,
                             guardian_telecom_use, travel_history_location1, travel_history_location2, travel_history_low,
                             travel_history_high, hco_root, hco_extension, hco_name, hco_telecom_use, hco_telecom_value,
                             hco_street, hco_city, hco_state, hco_zip, hco_county, hco_country, facility_root, facility_extension,
                             facility_name, facility_street, facility_city, facility_state, facility_zip, facility_county,
                             facility_country, provider_given_name, provider_family_name, provider_root, provider_extension,
                             provider_telecom_use, provider_telecom_value, provider_street, provider_city, provider_state,
                             provider_zip, provider_county, provider_country, software, software_version, encompassing_encounter,
                             encompassing_encounter_code, discharge_disposition, encounter_time, misc_notes, abort_med,
                             pregSupTimeLow, pregSupTimeHigh, pregSupDetMethodCode, pregSupDetMethodCodeSystem, pregSupDetMethodDisplay,
                             pregSupRecordDate, pregSupEstDelivDate, pregSupDelivDateMethodCode, pregSupDelivDateMethodCodeSystem,
                             pregSupDelivDateMethodDisplay, patGenderIdentityCode, patGenderIdentityCodeSystem, patGenderIdentityCode,
                             pregSupLastMenst, pregSupOutcomeCode, pregSupOutcomeCodeSystem, pregSupOutcomeDisplay, pregSupOutcomeTime,
                             PregSupPostPartStatusCode, PregSupPostPartStatusCodeSystem, PregSupPostPartStatusDisplay, resultOrgTriggerCode,
                             resultOrgTriggerCodeSystem, resultOrgTriggerDisplay, medAdminTriggerCode,medAdminTriggerCodeSystem,
                             medAdminTriggerDisplay, medPlannedCode, medPlannedCodeSystem, medPlannedDisplay,
                             medPlannedTriggerCode, medPlannedTriggerCodeSystem, medPlannedTriggerDisplay, medCodeCode, medCodeCodeSystem,
                             medCodeDisplay, medTriggerCode, medTriggerCodeSystem, medTriggerDisplay, immuVaccTrigCode, immuVaccTrigCodeSystem,
                             immuVaccTrigDisplay, travelPurpCode, travelPurpCodeSystem, travelPurpDisplay, travelTypeCode, travelTypeCodeSystem,
                             travelTypeDisplay, travelTransDetailCode, travelTransDetailCodeSystem, travelTransDetailDisplay, travelTransDetailValue,
                             occupationCurrentCode, occupationCurrentCodeSystem, occupationCurrentDisplay, occupationUsualCode, occupationUsualCodeSystem, occupationUsualDisplay,
                             industryCurrentCode, industryCurrentCodeSystem, industryCurrentDisplay, industryUsualCode, industryUsualCodeSystem, industryUsualDisplay, currentEmployerName, currentEmployerPhone,
                             currentEmployerAddressStreet, currentEmployerAddressCounty, currentEmployerAddressCity,currentEmployerAddressState,
                             currentEmployerAddressZip, currentEmployerAddressCountry, ocupationExposure, EmploymentStatusCode, EmploymentStatusCodeSystem, EmploymentStatusDisplay,
                             pregSupEstGestAge, pregSupEstGestAgeDate, pregSupEstGestAgeMethodCode, pregSupEstGestAgeMethodCodeSystem,  pregSupEstGestAgeMethodDisplay,
                             medHistCode, medHistCodeSystem, medHistDisplay, medHistText, systemsReviewText, specimenSourceCode, specimenSourceCodeSystem,
                             specimenSourceDisplay, specimenTypeCode, specimenId, specimentCollectDate, vitalsValue, vitalsUnit, medTherRespValueCode, medTherRespValueCodeSystem, medTherRespValueDisplay, homelessFlag,
                             procActCode, procActCodeSystem, procActCodeDisplay, procObsCode, procObsCodeSystem, procObsDisplay, procCode,
                             procCodeSystem, procDisplay, procTriggerActCode, procTriggerActCodeSystem, procTriggerActDisplay, procTriggerObsCode,
                             procTriggerObsCodeSystem, procTriggerObsDisplay, procTriggerProcCode, procTriggerProcCodeSystem, procTriggerProcDisplay,
                             procPlannedActCode, procPlannedActCodeSystem, procPlannedActDisplay, procPlannedProcCode, procPlannedProcCodeSystem, procPlannedProcDisplay,
                             procPlannedObsCode, procPlannedObsCodeSystem, procPlannedObsDisplay,
                             procPlannedTrigObsCode, procPlannedTrigObsCodeSystem, procPlannedTrigObsDisplay, procPlannedTriggerProcCode, procPlannedTriggerProcCodeSystem,
                             procPlannedTriggerProcDisplay, disabilityStatusCode, disabilityStatusCodeSystem, disabilityStatusDisplay, emergencyOutbreakCode,
                             emergencyOutbreakCodeSystem, emergencyOutbreakDisplay, exposureInfoCode, exposureInfoCodeSystem, exposureInfoDisplay, tribalAffiliationCode,
                             tribalAffiliationCodeSystem, tribalAffiliationDisplay, vaccineCredPatAssertCode, vaccineCredPatAssertCodeSystem, vaccineCredPatAssertDisplay,
                             nationalityCountryCode, nationalityCountryCodeSystem, nationalityCountryDisplay, residenceCountryCode, residenceCountryCodeSystem, residenceCountryDisplay]) ## Writes the values from the xml to the csv file
                                         
                                         
                except Exception as e:
                    PrintException()

zipEnd = time.time()
zipTime = zipEnd-startTime
print(f"Time to complete zip parsing: {zipTime/60}")

