# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

authors_csv = pd.DataFrame(
    {
        'user_id': [],
        'author': [],
        'affiliation': []
    }
)
papers_csv = pd.DataFrame(
    {
        'title': [],
        'authors': [],
        'publication_date': [],
        'description': [],
        'cite_by': []
    }
)

# %%
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://scholar.google.com/citations?view_op=view_org&hl=en&num=20&org=10241031385301082500")
#print(driver.title)

pageNumber = 0
while True:
    
    print("Page : "+str(pageNumber))

    profiles = driver.find_elements_by_class_name('gsc_1usr')
    profiles_name = []
    
    for profile in profiles:
        profiles_name.append(profile.find_element_by_tag_name('img').get_attribute('alt'))
    
    authors_name_in = driver.find_elements_by_class_name('gsc_1usr')
    for p_num in authors_name_in:
        author_data = []
        author_data.append(p_num.find_element_by_css_selector("h3.gs_ai_name").find_element_by_css_selector('a').get_attribute('href').split('=')[2])
        author_data.append(p_num.find_element_by_css_selector("h3.gs_ai_name").text)
        author_data.append(p_num.find_element_by_css_selector("div.gs_ai_aff").text)

        authors_csv = authors_csv.append(
            {
                'user_id':author_data[0],
                'author':author_data[1],
                'affiliation':author_data[2]
            }, ignore_index=True
        )

    for names in profiles_name:
        
        driver.find_element_by_css_selector("img[alt='{}']".format(names)).click()

        x = True
        while x != False:

            click_more = driver.find_element_by_css_selector("button[id='gsc_bpf_more']")
            attrs = driver.execute_script(
                'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', click_more)

            if(len(attrs)==4):
                x = False
            else:
                more_ariticles = driver.find_element_by_css_selector("button[id='gsc_bpf_more']").click()
                time.sleep(0.5)
        
        for i in driver.find_elements(By.CSS_SELECTOR, "td.gsc_a_t"):

            paper_data = []

            time.sleep(0.5)
            click_articles = i.find_element_by_css_selector("a.gsc_a_at").click()

            time.sleep(2)
            try:
                title_ = driver.find_element_by_css_selector("div[id='gsc_vcd_title']").text
            except:
                title_ = ("-")
            try:
                authors_ = driver.find_elements_by_css_selector('div.gsc_vcd_value')[0].text
            except:
                authors_ = ("-")
            try:
                public_date = driver.find_elements_by_css_selector('div.gsc_vcd_value')[1].text
            except:
                public_date = ("-")
            try:
                description_ = driver.find_element_by_css_selector("div[id='gsc_vcd_descr']").text
            except:
                description_ = ("-")
            try:
                cite_by_ = (driver.find_element_by_css_selector("div[style='margin-bottom:1em']").find_element_by_css_selector('a').text.split(' ')[2])
            except:
                cite_by_ = ("-")

            papers_csv = papers_csv.append(
                {
                    'title':title_,
                    'authors': authors_,
                    'publication_date': public_date,
                    'description': description_,
                    'cite_by': cite_by_
                }, ignore_index=True
            )
            driver.find_element_by_css_selector("a[id='gs_md_cita-d-x']").click()

        driver.back()
        time.sleep(1)

    try:
        print(driver.find_element_by_css_selector("span[class='gs_nph gsc_pgn_ppn']").text)
        if(driver.find_element_by_css_selector("span[class='gs_nph gsc_pgn_ppn']").text == "291 - 298"):

            authors_csv.to_csv('authors.csv')
            papers_csv.to_csv('papers.csv')

            print("FINISHED")
            driver.quit()
            break
        else:
            navigation = driver.find_element_by_css_selector("button[aria-label='Next']").click()
            pageNumber+=1
            time.sleep(1)
    except:
        break

# %%
import pandas as pd

df = pd.read_csv('authors.csv')
df
# %%
import pandas as pd

df1 = pd.read_csv('papers.csv')
df1