import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

class TacoBellSpider(scrapy.Spider):
    name = 'taco_nav'
    allowed_domains = ['tacobell.com']
    start_urls = ['https://www.tacobell.com/locations']

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse,
            wait_time=30,
            meta={'selenium': True}
        )

    def parse(self, response):
        driver = response.meta.get('driver')
        if not driver:
            self.logger.error('Driver not found in response meta')
            return

        self.enter_location(driver, 'Fredericksburg')

        try:
            self.logger.info('Waiting for address elements to load...')
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_store-result-card__3CyS6'))
            )
            self.logger.info('Address elements loaded.')

            address = driver.find_element(By.CSS_SELECTOR, 'div.styles_store-result-card__3CyS6')
            address_text = address.find_element(By.CSS_SELECTOR, 'div.styles_address-section__3nk0j').text
            distance = address.find_element(By.CSS_SELECTOR, 'span.styles_distance__7fJCV').text
            store_page = address.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            directions = address.find_element(By.CSS_SELECTOR, 'a[href*="google.com/maps/dir"]').get_attribute('href')
            method_details = address.find_element(By.CSS_SELECTOR, 'div.styles_method-item-details__3Qgjo').text
            button_text = address.find_element(By.CSS_SELECTOR, 'button.styles_button__FFI6b').text

            try:
                start_order_button = WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                      'button.styles_button__FFI6b.styles_button__1NHMg.styles_inverse__3KjTi.styles_brand__2fVUP'))
                )
                self.logger.info('Start Your Order button is visible and clickable.')
                driver.execute_script("arguments[0].click();", start_order_button)
                self.logger.info('Clicked on the "Start Your Order" button using JavaScript.')

                # Wait for the next elements to load
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_pickup-methods__33HdU'))
                )
                self.logger.info('Pickup methods loaded.')

                try:
                    start_order_button_pickup = WebDriverWait(driver, 60).until(
                        EC.visibility_of_element_located((By.XPATH, '//div[@class="styles_pickup-methods__33HdU"]/button[1]'))
                    )
                    self.logger.info('Start Your Order button pickup is visible and clickable.')
                    driver.execute_script("arguments[0].click();", start_order_button_pickup)
                    self.logger.info('Clicked on the "Start Your Order pickup" button using JavaScript.')

                    # Wait for the next elements to load
                    WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_border__2bei-.styles_primary__1bruE.styles_method-card__36eJx.styles_method-card-default__3eOsX'))
                    )
                    self.logger.info('Pickup methods loaded.')

                    try:
                        start_order_button_now = WebDriverWait(driver, 60).until(
                            EC.visibility_of_element_located((By.XPATH, "(//div[@class='styles_border__2bei- styles_primary__1bruE styles_method-card__36eJx styles_method-card-default__3eOsX'])[1]"))
                        )
                        self.logger.info('Start Your Order button now is visible and clickable.')
                        driver.execute_script("arguments[0].click();", start_order_button_now)
                        self.logger.info('Clicked on the "Start Your Order now" button using JavaScript.')

                        # Wait for the next elements to load
                        WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.XPATH, '//a[@class="styles_link-button__29UpC styles_bg-brand__2FGaD"]'))
                        )
                        self.logger.info('Pickup methods loaded.')

                        try:
                            start_order_button_finish = WebDriverWait(driver, 60).until(
                                EC.presence_of_element_located((By.XPATH, '//a[@class="styles_link-button__29UpC styles_bg-brand__2FGaD"]'))
                            )

                            self.logger.info('Start Your Order button finish is visible and clickable.')
                            driver.execute_script("arguments[0].scrollIntoView(true);", start_order_button_finish)
                            driver.execute_script("arguments[0].click();", start_order_button_finish)
                            self.logger.info('Clicked on the "Start Your Order finish" button')


                            # Wait for the next elements to load
                            WebDriverWait(driver, 60).until(
                                EC.presence_of_element_located((By.XPATH, '//article[@class="styles_card__1se34"]'))
                            )
                            self.logger.info('Pickup methods loaded.')


                        except TimeoutException as e:
                            self.logger.error(f"Timeout occurred while clicking 'Start Your Order': {e}")

                        except NoSuchElementException as e:
                            self.logger.error(f"Element not found while clicking 'Start Your Order': {e}")

                        except Exception as e:
                            self.logger.error(f"An error occurred while clicking 'Start Your Order': {e}")


                    except TimeoutException as e:
                        self.logger.error(f"Timeout occurred while clicking 'Start Your Order': {e}")

                    except NoSuchElementException as e:
                        self.logger.error(f"Element not found while clicking 'Start Your Order': {e}")

                    except Exception as e:
                        self.logger.error(f"An error occurred while clicking 'Start Your Order': {e}")


                except TimeoutException as e:
                    self.logger.error(f"Timeout occurred while clicking 'Start Your Order': {e}")

                except NoSuchElementException as e:
                    self.logger.error(f"Element not found while clicking 'Start Your Order': {e}")

                except Exception as e:
                    self.logger.error(f"An error occurred while clicking 'Start Your Order': {e}")


            except TimeoutException as e:
                self.logger.error(f"Timeout occurred while clicking 'Start Your Order': {e}")

            except NoSuchElementException as e:
                self.logger.error(f"Element not found while clicking 'Start Your Order': {e}")

            except Exception as e:
                self.logger.error(f"An error occurred while clicking 'Start Your Order': {e}")


            yield {
                'address': address_text,
                'distance': distance,
                'store_page': store_page,
                'directions': directions,
                'method_details': method_details,
                'button_text': button_text,
            }

        except TimeoutException as e:
            self.logger.error(f"Timeout occurred: {e}")

        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {e}")

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")


        finally:
            driver.quit()

    def enter_location(self, driver, location):
        try:
            # Handle cookie consent
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
                ).click()
                logging.info('Cookie consent accepted.')
            except TimeoutException:
                logging.warning('Cookie consent button not found. Continuing without accepting.')

            # Wait for the input field to be present and visible
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.styles_store-input__3vFqj'))
            )
            logging.info('Input field is visible.')

            # Use JavaScript to ensure the input field is interactive
            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.find_element(By.CSS_SELECTOR, 'input.styles_store-input__3vFqj'))

            # Wait for the input field to be clickable
            input_field = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.styles_store-input__3vFqj'))
            )
            logging.info('Input field is clickable.')

            # Use JavaScript to enter the value directly
            driver.execute_script("arguments[0].value = arguments[1];", input_field, location)

            # Optionally trigger any events that might be required
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_field)

            # Find and click the submit button
            submit_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.styles_button__27tOv'))
            )
            submit_button.click()

            # Optional: Wait for some results to load or handle the new page
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_address-section__3nk0j'))
            )

        except TimeoutException as e:
            logging.error(f"Timeout while interacting with elements: {e}")

        except NoSuchElementException as e:
            logging.error(f"Element not found: {e}")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

