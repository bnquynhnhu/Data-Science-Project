from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pyodbc 
import pandas as pd
from fake_useragent import UserAgent

PROG_LANGUAGE = ['R', 'Python', 'Java', 'C++', 'Ruby', 'Perl', 'Matlab', 'JavaScript', 'Scala']
ANALYSIS_TOOLS = ['PowerBI', 'Excel', 'Tableau', 'SAS', 'SPSS', 'SAP', 'QlikView', 'Data Studio']  
HADOOP_LST = ['Spark', 'AWS', 'Azure', 'Hadoop', 'Kafka', 'Scala', 'Hive', 'MapReduce']
DATABASE_LST = ['SQL', 'NoSQL', 'ElasticSearch', 'PostgreSQL', 'MongoDB', 'Cassandra', 'Oracle', 'HBase']  
LIBRARY_LST = ['Tensorflow', 'SciKit-learn','Statsmodels', 'Keras', 'PyTorch', 'NLTK', 'pandas']
DS_SKILLS = ['Machine Learning', 'Data Analysis','Data Mining', 'NLP', 'Data Visualization', 'Statistics', 'Deep Learning', 'Big Data', 'Computer Vision', 'Artificial Intelligence']
DB_SERVER = 'DESKTOP-60QTTQN\MSSQLSERVER03' 
DATABASE = 'indeed'
SCRAPING_URL = "https://fr.indeed.com"
SERVERNAME = "DESKTOP-60QTTQN\MSSQLSERVER03"
LOGFILE = "logfilename.log"

DS_SKILLS = PROG_LANGUAGE + ANALYSIS_TOOLS + HADOOP_LST + DATABASE_LST + LIBRARY_LST + DS_SKILLS

ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]
n = 1

def replaceKeyWords(txt):
    src_str  = re.compile('Analyse des données', re.IGNORECASE) 
    txt  = src_str.sub('Data Analysis', txt)
    src_str  = re.compile('Analyse de données', re.IGNORECASE) 
    txt  = src_str.sub('Data Analysis', txt)
    src_str  = re.compile('Dataviz', re.IGNORECASE) 
    txt  = src_str.sub('Data Visualization', txt)    
    src_str  = re.compile('Natural Language Processing', re.IGNORECASE) 
    txt  = src_str.sub('NLP', txt)
    src_str  = re.compile('Statistiques', re.IGNORECASE) 
    txt  = src_str.sub('Statistics', txt)
    src_str  = re.compile('Vision par Ordinateur', re.IGNORECASE) 
    txt  = src_str.sub('Computer Vision', txt)
    txt.replace('IA', 'Artificial Intelligence')
    txt.replace('AI', 'Artificial Intelligence')
    txt.replace('I.A.', 'Artificial Intelligence')
    txt.replace('Visualization', 'Artificial Intelligence')
    src_str  = re.compile('Qlik', re.IGNORECASE) 
    txt  = src_str.sub('QlikView', txt)
    
    return txt

def findOnlyWholeWord(search_string, input_string):
    # Create a raw string with word boundaries from the user's input_string
    raw_search_string = r"\b" + re.escape(search_string) + r"\b"
    match_output = re.search(raw_search_string, input_string, 
                             flags=re.IGNORECASE)
    
    no_match_was_found = (match_output is None)
    if no_match_was_found:
      return False
    else:
      return True
    
def extractDataScienceSkills(strJobDesc):
    strJobDesc = replaceKeyWords(strJobDesc)
    
    try:
        lstSkills = []
        for skill in DS_SKILLS:
            if findOnlyWholeWord(skill, strJobDesc):
                lstSkills.append(skill)
    except Exception as e:
        print("Error in extractDataScienceSkills", e)
        
    return lstSkills

def getURL(position, location, radius):
    url = SCRAPING_URL + "/jobs?q={}&l={}&radius={}"
    url = url.format(position, location, radius)
    return url

def getJobDetails(url):
    # Jump to Job Details page and scrape data
    browser = webdriver.Firefox()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    browser.quit()

    if (soup is not None):
        job_summary = soup.find("div", "jobsearch-jobDescriptionText")
        if (job_summary is not None):
            job_summary = job_summary.text.strip()
            skills = extractDataScienceSkills(job_summary)
            skills = ",".join(skills)
        else:
            skills = ""
            job_summary = ""
    
    return skills, job_summary
    
def getCompanyDetails(url):
    # Jump to Company Details page and scrape data
    browser = webdriver.Firefox()
    browser.get(url)
    html = browser.page_source
    company = BeautifulSoup(html, features="html.parser")
    browser.quit()

    if (company is not None):
        company_size = company.find(attrs={"data-testid": "companyInfo-employee"})
        if company_size is not None:
            company_size = company_size.find('div', 'css-1cljifo-Box')
            if company_size is not None:
                company_size = company_size.text.strip()
            else: company_size = ""
        else:
            company_size = ""
       
        company_revenue = company.find(attrs={"data-testid": "companyInfo-revenue"})
        if company_revenue is not None:
            company_revenue = company_revenue.find('div', 'css-1cljifo-Box')
            if company_revenue is not None:
                company_revenue = company_revenue.text.strip()
            else: company_revenue = ""
        else:
            company_revenue = ""
            
        company_industry = company.find(attrs={"data-testid": "companyInfo-industry"})
        if company_industry is not None:
            company_industry = company_industry.find('div', 'css-1cljifo-Box')
            if company_industry is not None:
                company_industry = company_industry.text.strip()
            else: company_industry = ""
        else:
            company_industry = ""
            
    return company_size, company_revenue, company_industry

def get_data(job, position):
    try:
        jobtitle = job.find('a', 'jobtitle').get('title')

        company_name = job.find('span', 'company')
        if company_name != None:
            company_name = company_name.getText().strip()
        else: company_name = ""
        
        company_url = job.find(attrs={"data-tn-element": "companyName"})

        if (company_url is not None):
            company_url = company_url.get('href')
            company_url = SCRAPING_URL + company_url if (company_url.startswith("/")) else company_url

            company_size, company_revenue, company_industry = getCompanyDetails(company_url)
        else:
            company_size = ""
            company_revenue = ""
            company_industry = ""

        job_location = job.find('div', 'recJobLoc').get('data-rc-loc')
        post_date = job.find('span', 'date').text.strip()
        if (post_date == "Aujourd'hui") or (post_date == "Publiée à l'instant"): 
            days = 0
        else:
            pattern="\d+"
            days = int(re.findall(pattern, post_date)[0])
        post_date = (datetime.now() - timedelta(days = days)).strftime('%Y-%m-%d')
        scrape_date = datetime.today().strftime('%Y-%m-%d')

        salary = job.find('span', 'salaryText')
        if (salary is not None):
            salary = salary.text.strip()
        else:
            salary = ""

        # Jump to job description page
        job_url = job.find('a', 'jobtitle').get('href')
        job_url = SCRAPING_URL + job_url if (job_url.startswith("/")) else job_url

        skills, job_summary = getJobDetails(job_url)

        return (jobtitle, job_url, job_location, post_date, \
                scrape_date, salary, skills, company_name, company_size, \
                        company_revenue, company_industry, position, 'Indeed')
    except Exception as e:
        print("Error in get_data: ", e)
        

def connectDB():
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port is not null

    conn = pyodbc.connect(r'Driver=SQL Server;Server='+SERVERNAME+';Database='+DATABASE+';Trusted_Connection=yes;')
    if (conn is not None):
        cursor = conn.cursor()
        return cursor, conn
    else:
        return None, conn
    
def disconnectDB(cursor):
    cursor.close()
    
def insert_SQLDB(cursor, conn, dbrows):
    if (cursor is not None):
        query = 'INSERT INTO job (jobtitle,'\
                        'joblink,'\
                        'job_location,'\
                        'post_date,'\
                        'scrape_date,'\
                        'salary,'\
                        'skills,'\
                        'company_name,'\
                        'company_size,'\
                        'company_revenue,'\
                        'company_industry,'\
                        'job_category,'\
                        'employment_site) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'

        try:
            cursor.executemany(query, dbrows)
            conn.commit()
            return True
        except Exception as e:
            print("Failed to insert values", e)
            return False
    else:
        print("Connection failed")      
        

def scrapingDataFromIndeed(position, location, rayon):
    ####url = getURL(position, location, rayon)
    url = "https://fr.indeed.com/jobs?q=data+analyst&l=France"

    while True:
        records = []  
        print("url", url)
  
        browser = webdriver.Firefox()
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
        
        # Find all jobs for this page
        jobs = soup.find_all('div', 'jobsearch-SerpJobCard')
        
        # Get the content of the next page
        try:
            url = SCRAPING_URL + "/" + soup.find('a', {'aria-label': 'Suivant'}).get('href')
        except Exception as e:
            print("Failed in scrapingDataForEachCity: ", e)
            break
            
        browser.quit()
        
        if (jobs is not None) and len(jobs)>0:
            for job in jobs:
                record = get_data(job, position)
                if record is not None: records.append(record)
    
            if ((records is not None) and (len(records) > 0)):
                cursor, conn = connectDB()
                print(records[0])
                success = insert_SQLDB(cursor, conn, records)
                disconnectDB(cursor)
                
                if success: print("Inserted ", len(records), " records for the city ", location)
                else: print("Failed to insert")
            else:
                print("No records found")
                

                
        else:
            break


if __name__ == "__main__":
    print("Web scraping has begun ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    scrapingDataFromIndeed('Data+Scientist', 'France', 0)
    print("Web scraping is now complete!", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))