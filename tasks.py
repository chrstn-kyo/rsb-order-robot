from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo=100,)
    open_robot_order_website()
    close_annoying_popup()
    orders = get_orders()
    loop_the_orders(orders)


    # orders = get_orders()
    # loop_the_orders(orders)

def open_robot_order_website():
    """ Opens the RobotSpareBin Industries Inc. website. """
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    """ Downloads the csv order file and return an order table """
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)
    tables = Tables()
    order_table = tables.read_table_from_csv("orders.csv", header=True)
    return order_table

def loop_the_orders(orders):
    """ Loops through the orders and processes them """
    for order in orders:
        fill_the_form(order)
        preview_the_robot()
        submit_the_order()    

def close_annoying_popup():
    """ Closes the annoying popup that appears on the website """
    page = browser.page()
    page.click("text=OK")

def fill_the_form(order):
    """ Fills the order form """
    page = browser.page()
    page.select_option("#head", str(order["Head"]))
    page.click("input[type='radio'][value='" + str(order["Body"]) + "']") #"input[type='radio'][value='medium']"
    page.fill("input[placeholder='Enter the part number for the legs']", str(order["Legs"]))
    page.fill("#address", order["Address"])

def preview_the_robot():
    """ Takes a screenshot of the robot """
    page = browser.page()
    page.click("text=preview")
    # browser.screenshot("robot.png")

def submit_the_order():
    """ Submits the order form """
    page = browser.page()
    while True:
        try:
            page.click("text=order")
            break
        except:
            print("Failed to submit order, trying again...")
