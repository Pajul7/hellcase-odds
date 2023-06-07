from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
url = input("Please enter a valid Hellcase case link :\n")

chrome_options = Options()  
chrome_options.add_argument("--headless") # Opens the browser up in background
print("Sarting headless browser...")
with Chrome(options=chrome_options) as browser:
    browser.implicitly_wait(15)
    browser.get(url)

    html = browser.page_source
    print("Getting Case on Hellcase.com...")
    items_global_probas = []
    items_local_ProbaPrice_tuple = []
    case_number = len(browser.find_elements(By.CLASS_NAME,"item-wrap"))
    current_case = 1
    case_price = float(browser.find_element(By.CLASS_NAME,"core-price--preset--default").get_attribute("textContent").strip()[1:])
    for item in browser.find_elements(By.CLASS_NAME,"item-wrap"):
        print("Getting global items odds...", int(current_case/case_number*100),"%")
        items_global_probas.append(
        round(float(item.find_element(By.CLASS_NAME,"item-wrap__chance").find_elements(By.TAG_NAME,"span")[1].get_attribute("textContent").strip()[:-1])/100,6)
        )
        button = item.find_element(By.CLASS_NAME,"item-wrap__button")
        button.click()

        oddsTable = item.find_element(By.CLASS_NAME,"odds-table")
        
        raretesItemValues = oddsTable.find_elements(By.CLASS_NAME,"base-price__value")

        raretesItemValuesrefined = [float(raretesItemValues[i]
                                    .get_attribute("textContent")
                                    .strip()) for i in range(len(raretesItemValues))]



        chancesraretesItem = [round(
                                    float(oddsTable
                                    .find_elements(By.CLASS_NAME,"odds-number")[i]
                                    .get_attribute("textContent")
                                    .strip()[:-1])/100,6)
                                    for i in range(1,len(raretesItemValuesrefined)+1)
                            ]

        items_local_ProbaPrice_tuple.append([raretesItemValuesrefined,chancesraretesItem])
        current_case +=1



Global_Items_Esperance = 0
temp = 0
for item_index in range(len(items_global_probas)):
    print("Calculating Item Expected Value of Item",item_index,"...")
    item_esperance = 0
    for qualite_index in range(len(items_local_ProbaPrice_tuple[item_index][0])):
        item_esperance+= items_local_ProbaPrice_tuple[item_index][0][qualite_index] * (items_local_ProbaPrice_tuple[item_index][1][qualite_index]/items_global_probas[item_index])

    Global_Items_Esperance+=item_esperance*items_global_probas[item_index]
print("\nExpected Value is",round(Global_Items_Esperance,4),"$\n")
print("Minus case Price : ",round(Global_Items_Esperance-case_price,4),"$\nAverage gain ;",round(100*((Global_Items_Esperance-case_price)/case_price),4),"%")


browser.quit()



