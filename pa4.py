# Homework 4 by Chris Nowak solving a webscraping problem
import pandas as pd
import bs4
from time import sleep
import requests

page = requests.get("http://collegecatalog.uchicago.edu/thecollege/anthropology/")

def important_info(page):
    ''' '''
    soup = bs4.BeautifulSoup(page.text, features = 'lxml')
    courses = soup.find_all("p", class_ = "courseblocktitle")    
    course_code_info = []
    course_name_info = []
    course_units_info = []
    for i in courses:
        text_info = i.text.split("  ")
        for j, k in enumerate (text_info):
            text_info[j] = k.replace(".", "").strip()
        if len(text_info[0].split('-')) < 2:
            course_code_info.append(text_info[0])
            course_name_info.append(text_info[1])
            course_units_info.append(text_info[2])
            
    info_df = pd.DataFrame({"Course Code": course_code_info,
                            "Course Name": course_name_info,
                            "Units": course_units_info})
    return info_df


def page_df(page):
    ''''''
    soup = bs4.BeautifulSoup(page.text, features = 'lxml')
    titles = soup.find_all("p", class_ = "courseblocktitle")
    descs = soup.find_all("p", class_ = "courseblockdesc") 
    details = soup.find_all("p", class_ = "courseblockdetail")   
    
    titles_code_info = []
    titles_name_info = []
    discard = []
    for i, title in enumerate(titles):
        text_info = title.text.split("  ")
        for j, k in enumerate (text_info):
            text_info[j] = k.replace(".", "").strip()
        if len(text_info[0].split('-')) < 2:
            titles_code_info.append(text_info[0])
            titles_name_info.append(text_info[1])
        else:
            discard.append(i)
            
    descs_info = []
    for i, j in enumerate(descs):
        if i  not in discard:
            descs_info.append(j.text.strip())
            
    detail_instructor_info = []
    detail_terms_info = []
    detail_prereq_info = []
    detail_equivalent_info = []
    detail_notes_info = []
    detail_info = []
    for i in details:
        detail_info.append(i.text.strip())
    
    key_w = ['Instructor(s):', "Terms Offered:",
             "Prerequisite(s):", "Equivalent Course(s):",
             "Note(s):"]
    
    for i in detail_info:
        key_lst = []
        value_lst = []
        raw_details = i
        for j, word in enumerate(key_w):
            if len(raw_details.split(word)) != 1:
                raw_details = " ".join(raw_details.split(word))
                key_lst.append(word)
            
        for sep in ['\xa0\xa0\xa0\xa0\xa0', '\n']:
            raw_details = " ".join(raw_details.split(sep))
            
        value_lst = raw_details.split('   ')
        for i, j in enumerate(value_lst):
            value_lst[i] = j.strip()
        
        detail_dict = {}
        for i in range(len(key_lst)):
            if len(key_lst) == len(value_lst):
                detail_dict.update({key_lst[i]: value_lst[i]})
            else:
                detail_dict.update({key_lst[i]: "None"})
        
        if 'Instructor(s):' in detail_dict.keys():
            detail_instructor_info.append(detail_dict['Instructor(s):'])
        else:
            detail_instructor_info.append('None')
            
        if 'Terms Offered:' in detail_dict.keys():
            detail_terms_info.append(detail_dict['Terms Offered:'])
        else:
            detail_terms_info.append('None')
            
        if 'Prerequisite(s):' in detail_dict.keys():
            detail_prereq_info.append(detail_dict['Prerequisite(s):'])
        else:
            detail_prereq_info.append('None')
            
        if 'Equivalent Course(s):' in detail_dict.keys():
            detail_equivalent_info.append(detail_dict['Equivalent Course(s):'])
        else:
            detail_equivalent_info.append('None')
            
        if 'Note(s):' in detail_dict.keys():
            detail_notes_info.append(detail_dict['Note(s):'])
        else:
            detail_notes_info.append('None')
            
    info_df = pd.DataFrame({"Course Code": titles_code_info,
                            "Course Name": titles_name_info,
                            "Course Description": descs_info,
                            "Instructor(s)": detail_instructor_info,
                            "Terms Offered": detail_terms_info,
                            "Prerequisite(s)": detail_prereq_info,
                            "Equivalent Courses": detail_equivalent_info,
                            "Notes": detail_notes_info})
    
    return info_df

baseurl = "http://collegecatalog.uchicago.edu"
def next_page(page, n):
    ''''''
    soup = bs4.BeautifulSoup(page.text, features='lxml')
    links = soup.find_all("a", href=True)[11:80]
    return baseurl + links[n].attrs["href"]

page = requests.get("http://collegecatalog.uchicago.edu/thecollege/anthropology/")
def all_courses(page):
    ''''''
    full_df = pd.DataFrame({})
    for i in range(69):
        if i == 0:
            full_df = pd.concat([full_df, page_df(page)], axis=1)
        else:
            full_df = pd.concat([full_df, page_df(page)])
        nexturl = next_page(page, i)
        print("Sleeping")
        sleep(3)
        print("Retrieving", nexturl)
        page = requests.get(nexturl)
    return full_df

def most_classes(page):
    max_df = pd.DataFrame({})
    for i in range(69):
        if len(page_df(page)) > len(max_df):
            max_df = page_df(page)
        nexturl = next_page(page, i)
        print("Sleeping")
        sleep(3)
        print("Retrieving", nexturl)
        page = requests.get(nexturl)
    return max_df

 all_courses = all_courses(page)
print(all_courses)
all_courses.to_csv('/Users/christophernowak/Downloads/hw4-ChNowak/course_catalog.csv')

print()

department = most_classes(page)
print(department)
department.to_csv('/Users/christophernowak/Downloads/hw4-ChNowak/largest_department.csv')