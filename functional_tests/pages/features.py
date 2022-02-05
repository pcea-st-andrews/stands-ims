from selenium.webdriver.common.by import By

from . import components
from .base import BasePage


class HomePage(BasePage):
    PATH = "/"
    SIGN_UP_LINK = (By.ID, "signup")
    LOGIN_LINK = (By.ID, "login")

    @property
    def signup_link(self):
        element = self.browser.find_element(*self.SIGN_UP_LINK)
        return {element.text: element.get_attribute("href")}

    @property
    def login_link(self):
        element = self.browser.find_element(*self.LOGIN_LINK)
        return {element.text: element.get_attribute("href")}


class Dashboard(BasePage):
    PATH = "/dashboard/"


class PeopleListPage(BasePage):
    PATH = "/people/"

    @property
    def form(self):
        return components.SearchForm(self.browser)

    @property
    def table(self):
        return components.PeopleTable(self.browser)


class TemperatureRecordsListPage(BasePage):
    PATH = "/records/temperature/"

    @property
    def form(self):
        return components.SearchForm(self.browser)

    @property
    def table(self):
        return components.Table(self.browser)


class TemperatureRecordCreationPage(BasePage):
    def __init__(self, test, person_username):
        super().__init__(test)
        self.person_username = person_username

    @property
    def PATH(self):
        return f"/records/temperature/{self.person_username}/add/"

    @property
    def form(self):
        return components.TemperatureRecordCreationForm(self.browser)

    def add_temperature(self, temperature):
        self.form.send_keys(temperature=temperature)
        return self


class PersonCreationPage(BasePage):
    PATH = "/people/add/"

    @property
    def form(self):
        return components.PersonForm(self.browser)

    def add_person(self, username, full_name, gender, dob):
        self.form.send_keys(
            username=username, full_name=full_name, gender=gender, dob=dob
        )
        return self


class AdultCreationPage(PersonCreationPage):
    PATH = "/people/add/adult/"

    @property
    def form(self):
        return components.AdultForm(self.browser)

    def add_person(self, username, full_name, gender, dob, phone_number):
        self.form.send_keys(
            username=username,
            full_name=full_name,
            gender=gender,
            dob=dob,
            phone_number=phone_number,
        )
        return self


class AdultSelfRegistrationPage(AdultCreationPage):
    PATH = "/people/register/self/"


class ChildCreationPage(PersonCreationPage):
    PATH = "/people/add/child/"

    @property
    def form(self):
        return components.ChildForm(self.browser)

    def add_person(self, username, full_name, gender, dob, is_parent=False):
        self.form.send_keys(
            username=username,
            full_name=full_name,
            gender=gender,
            dob=dob,
            is_parent=is_parent,
        )
        return self


class PersonDetailPage(BasePage):
    UPDATE_LINK = (By.ID, "update")

    def __init__(self, test, person_username):
        super().__init__(test)
        self.person_username = person_username

    @property
    def PATH(self):
        return f"/people/{self.person_username}/"

    @property
    def _update_link_element(self):
        return self.browser.find_element(*self.UPDATE_LINK)

    @property
    def update_link(self):
        element = self._update_link_element
        return {element.text: element.get_attribute("href")}

    def update_person(self):
        self._update_link_element.click()


class PersonUpdatePage(BasePage):
    def __init__(self, test, person_username):
        super().__init__(test)
        self.person_username = person_username

    @property
    def PATH(self):
        return f"/people/{self.person_username}/update/"

    @property
    def form(self):
        return components.PersonForm(self.browser)

    def update_person(self, username=None, full_name=None, gender=None, dob=None):
        self.form.send_keys(
            username=username, full_name=full_name, gender=gender, dob=dob
        )
        return self


class InterpersonalRelationshipsListPage(BasePage):
    PATH = "/people/relationships/"

    @property
    def form(self):
        return components.SearchForm(self.browser)

    @property
    def table(self):
        return components.Table(self.browser)


class InterpersonalRelationshipCreationPage(BasePage):
    PATH = "/people/relationships/add/"

    @property
    def form(self):
        return components.InterpersonalRelationshipCreationForm(self.browser)

    def add_relationship(self, person_username, relative_username, relationship_type):
        self.form.send_keys(
            person_username=person_username,
            relative_username=relative_username,
            relationship_type=relationship_type,
        )
        return self


class ParentChildRelationshipCreationPage(BasePage):
    def __init__(self, test, child_username):
        super().__init__(test)
        self.child_username = child_username

    @property
    def PATH(self):
        return f"/people/relationships/add/{self.child_username}/parent/"

    @property
    def form(self):
        return components.ParentChildRelationshipCreationForm(self.browser)

    def add_parent(self, parent_username):
        self.form.send_keys(parent_username=parent_username)
        return self
