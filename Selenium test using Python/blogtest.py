from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="post_nest",
    user="postgres",
    password="666666",
    # port: 5432
    )
cursor = conn.cursor()

# keep chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# create and configure the Chrome webdriver
driver = webdriver.Chrome(options = chrome_options)

# finding id function
def finding_id(postCon):
    cursor.execute("SELECT * FROM posts")
    # Fetch data
    data = cursor.fetchall()
    for row in data:
        if row[3] == postCon:
            idF = row[0]
    return idF
# finding post function
def finding_post(idNum):
    cursor.execute("SELECT * FROM posts WHERE id ="+str(idNum))
    post = cursor.fetchone()
    return post

# Navigate to web page
driver.get("http://localhost:2000/")

# verify whether the web page load success
assert driver.title == "Blog Web", f"Page title incorrect: {driver.title}"
print("✅ Page loaded successfully!")

# test the inputs element in the home page and new_post button
author = driver.find_element(By.NAME, "author").send_keys("author")
subject = driver.find_element(By.NAME, "subject").send_keys("subject")
post = driver.find_element(By.NAME, "post").send_keys("post")
newpo_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div/div[3]/button').click()

# verify post request success
success_msg = driver.find_element(By.ID, "suc").text
assert "New post created successfully." in success_msg, "❌ Form submission failed!"
print("✅ New post created successfully!")

# test the edit button under the existing post
post_existing = "post"
targetId = finding_id(post_existing)
edit_button = driver.find_element(By.ID, "edit"+str(targetId))
driver.execute_script("arguments[0].scrollIntoView();", edit_button)
time.sleep(2)
edit_button.click()

# verify button clicked successfully
WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:2000/"))
assert driver.current_url != "http://localhost:2000/", "❌ Button click failed!"
print("✅ Button clicked successfully, and URL changed!")

# test the edit page
au_edit = driver.find_element(By.NAME, "author").send_keys(" edit")
sub_edit = driver.find_element(By.NAME, "subject").send_keys(" edit")
po_edit = driver.find_element(By.NAME, "post").send_keys(" edit")
editPo_button = driver.find_element(By.XPATH, '/html/body/div[1]/form/div/div/div[3]/button').click()

# verify post has been changed successfully
edit_msg = driver.find_element(By.CSS_SELECTOR, '.post'+str(targetId)+' h4').text
assert "subject edit" in edit_msg, "❌ Form submission failed!"
print("✅ Post has been changed successfully!")

# test the delete button
post_edit = "post edit"
targetId2 = finding_id(post_edit)
delete_button = driver.find_element(By.ID, "delete"+str(targetId2))
driver.execute_script("arguments[0].scrollIntoView();", delete_button)
time.sleep(2)
delete_button.click()

# verify post has been deleted succcessfully
time.sleep(1)
post_deleted = finding_post(targetId2)
if not post_deleted:
    print("✅ Post has been deleted successfully!")
else:
    print("❌ Post still exists in the database!")

# test Features button
time.sleep(1)
features_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/footer/ul/li[2]/a')
driver.execute_script("arguments[0].scrollIntoView();", features_button)
time.sleep(2)
features_button.click()

# Features button clicked successfully
WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:2000/"))
assert driver.current_url != "http://localhost:2000/", "❌ Features Button click failed!"
print("✅ Features Button clicked successfully, and URL changed!")

# test home button in the Features page
time.sleep(1)
home_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/footer/ul/li[1]/a')
driver.execute_script("arguments[0].scrollIntoView();", home_button)
time.sleep(2)
home_button.click()

# Features button clicked successfully
WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:2000/features"))
assert driver.current_url != "http://localhost:2000/features", "❌ Home Button click failed!"
print("✅ Home Button clicked successfully, and URL changed!")

# close the connection
cursor.close()
conn.close()
