def getAttendance(driver):
    try:
        events = driver.find_element(By.ID, 'webtlasteventsbody')
        lastEvent = events.find_elements(By.XPATH, './/*')[2]
        lastEventHTML = lastEvent.get_attribute('innerHTML')
    except Exception as err:
        print(err, file=sys.stderr)
        return None

    if(lastEventHTML.find('Příchod') != -1):
        return True

def makeAction(driver, action):
    try:
        className = 'btn-primary' if action else 'btn-secondary'
        button = driver.find_element(By.CLASS_NAME, className)
        button.click()

def flipAttendance(driver):
    event = getLastEvent(driver)

    if(event == None):
        print("Couldn't get last event", file=sys.stderr)
        return True

    print("The last event was", 'arrival' if event else 'departure')

    if(makeAction(driver, not event)):
        print("Couldn't make action")
        return True

    time.sleep(2)

    newEvent = getLastEvent(driver)

    if(newEvent == None):
        print("Couldn't get last event", file=sys.stderr)
        return True

    if(event == newEvent):
        print("Action wasn't executed properly", file=sys.stderr)
        return True

    return False

