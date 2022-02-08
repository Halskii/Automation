import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# This uses a local text file to parse email, password, and cvv information.
with open('bot_account.txt', 'r') as file:
    email, password, cvv = file.read().splitlines()

# Item purchasing bot (for Best Buy).
class CheckOutBot:

    # Opens up our webpage.
    def __init__(self):

        # In the line below: Specify a path where you've downloaded 'chromedriver.exe' for selenium.
        self.driver = webdriver.Chrome('C:\\Users\\something\\something\\chromedriver.exe')
        self.driver.get("https://www.bestbuy.com/")
    
    # Logs you into Best Buy account using stored information. 
    def login(self, email, password):

        # Goes to the my account webpage.
        self.driver.get("https://www.bestbuy.com/site/customer/myaccount")
        time.sleep(3)
        
        # Fills out email field.
        email_input = self.driver.find_element_by_id("fld-e")
        email_input.clear()
        email_input.send_keys(email)

        # Fills out password field.
        pass_input = self.driver.find_element_by_id("fld-p1")
        pass_input.clear()
        pass_input.send_keys(password)
        time.sleep(2)

        # Clicks login button.
        self.driver.find_elements_by_class_name("cia-form__controls ")[0].click()
        time.sleep(2)

    # Attempts to add an item to your Best Buy cart.
    def add_product_to_cart(self, link):
       
        # Goes to designated product page.
        self.driver.get(link)
        time.sleep(1)

        # Loop attempts to add the item to cart, refreshes page until it is possible.
        while True:
            try:
                # Identifys the add to cart button.
                add_to_cart_button = self.driver.find_element_by_xpath('//button[normalize-space()="Add to Cart"]')
                try:
                    # Determines if we can click add to cart button. (It will be grayed out otherwise)
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button")))
                    driver_click(driver, 'css', '.add-to-cart-button')
                    time.sleep(5)
                    driver.refresh()
                    time.sleep(5)
                except Exception:
                    print("Queue Error")

                break
            except Exception:
                # Refreshes the page if we couldn't find the clickable add to cart button.
                self.driver.refresh()
                time.sleep(3)

        # Clicks add to cart.
        add_to_cart_button.click()
        self.driver.refresh()
        time.sleep(2)

    # Purchases item in cart.
    def checkout(self):

        # Goes to cart URL.
        self.driver.get("https://www.bestbuy.com/cart")
        time.sleep(1)

        # Finds the checkout button and clicks it.
        checkout_button = self.driver.find_element_by_xpath('//button[normalize-space()="Checkout"]')
        checkout_button.click()
        time.sleep(1)

        # Fills the CVV field withe the stored CVV information.
        #   Note: This assumes you're using a card saved to your Best Buy profile.
        cvvField = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.ID, "credit-card-cvv"))
        )
        cvvField.send_keys(cvv)

        # Finds place order button and completes purchase.
        checkout_button = self.driver.find_element_by_xpath('//button[normalize-space()="Place Your Order"]')
        checkout_button.click()
        time.sleep(1)

    def __del__(self):
        self.driver.close()

if __name__ == "__main__":
    checkout_bot = CheckOutBot()

    # Logs into Best Buy using the stored email and password.
    checkout_bot.login(email, password)

    # Adds item to cart.
    checkout_bot.add_product_to_cart(
        #   Best Buy Product URL Below
        "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"
    )
    # Attempts to purchase item in cart.
    checkout_bot.checkout()
    time.sleep(5)
