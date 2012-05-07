#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from base import Base
from common import wait_until_element
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from robot.api import logger
from robot.utils import asserts


class org(object):

    #ROBOT_LIBRARY_SCOPE = 'TEST_CASE'
    __version__ = '0.1'


    # Locators
    _HEADER_ORGANIZATIONS = "//li[@id='organizations']/a"
    _NEW_ORG_LINK = "//div[@id='list-title']/header/a"
    _ORG_NAME = "//form[@id='new_organization']/fieldset/div[2]/input"
    _ORG_SUBMIT = "//form[@id='new_organization']/div[2]/div/input"
    _NEW_ORG = "//div[@id='organization_%s']/div"


    def __init__(self):
        self.base = Base()


    def go_to_organizations_tab(self):
        """
        Takes user to the Organizations tab in the ui.
        """

        # Organizations tab
        organizations_tab = wait_until_element(self.base.driver, self._HEADER_ORGANIZATIONS, By.XPATH)
        asserts.fail_if_none(organizations_tab, "Could not find the Organizations tab.")
        organizations_tab.click()


    def select_org(self, org_name):
        """
        Switch the ui context to the provided org name.
        """

        # go to the url
        self.base.driver.get(self.base.base_url)

        # Check for the Organizations selector
        orgbox = wait_until_element(self.base.driver, "//a[@id='switcherButton']/div", By.XPATH)
        asserts.fail_if_none(orgbox, "Could not locate the Organizations selector.")
        orgbox.click()

        # Select the organization
        org = wait_until_element(self.base.driver, "//a[contains(., '%s')]" % org_name.replace(" ", "_"), By.XPATH)
        asserts.fail_if_none(org, "Could not locate the '%s' organization." % org_name)
        org.click()

        # Validate organization changed
        orgbox = wait_until_element(self.base.driver, "//a[@id='switcherButton']/div", By.XPATH)
        asserts.fail_if_none(orgbox, "Could not locate the Organizations selector.")
        asserts.assert_equal(orgbox.text, org_name, "Failed to swith to the '%s' organization." % org_name)


    def create_org(self, name):
        """
        Creates a new organization with the provided name.
        """

        # go to the url
        self.base.driver.get(self.base.base_url)

        # Select the Organizations tab
        self.go_to_organizations_tab()

        # Orgs List link
        org_list_link = wait_until_element(self.base.driver, "//li[@id='org_list']/a", By.XPATH)
        asserts.fail_if_none(org_list_link, "Could not find the Orgs List link.")
        org_list_link.click()

        # Verify that org doesn't exist
        org = wait_until_element(self.base.driver, self._NEW_ORG % name.replace(" ", "_"), By.XPATH)
        asserts.fail_unless_none(org, "An organization named '%s' already exists." % name)

        # New Organization link
        new_org_link = wait_until_element(self.base.driver, self._NEW_ORG_LINK, By.XPATH)
        asserts.fail_if_none(new_org_link, "could not find the new organization link.")
        new_org_link.click()

        # New org form
        org_name = wait_until_element(self.base.driver, self._ORG_NAME, By.XPATH)
        asserts.fail_if_none(org_name, "Could not enter the organization name.")
        org_name.send_keys(name)

        submit_button = wait_until_element(self.base.driver, self._ORG_SUBMIT, By.XPATH)
        submit_button.click()

        # Orgs List link
        org_list_link = wait_until_element(self.base.driver, "//li[@id='org_list']/a", By.XPATH)
        asserts.fail_if_none(org_list_link, "Could not find the Orgs List link.")
        org_list_link.click()

        # Verify that new org exists
        org = wait_until_element(self.base.driver, self._NEW_ORG % name.replace(" ", "_"), By.XPATH)
        asserts.fail_if_none(org, "Could not locate the newly created organization named '%s'." % name)


    def delete_org(self, name):
        """
        Creates a new organization with the provided name.
        """

        # go to the url
        self.base.driver.get(self.base.base_url)

        # Select the Organizations tab
        self.go_to_organizations_tab()

        # Orgs List link
        org_list_link = wait_until_element(self.base.driver, "//li[@id='org_list']/a", By.XPATH)
        asserts.fail_if_none(org_list_link, "Could not find the Orgs List link.")
        org_list_link.click()

        # Verify that org exists
        org = wait_until_element(self.base.driver, self._NEW_ORG % name.replace(" ", "_"), By.XPATH)
        asserts.fail_if_none(org, "Could not locate an organization named '%s'." % name)
        org.click()

        # Remove Org link
        remove_org_link = wait_until_element(self.base.driver, "//div[@id='panel']/div/div[2]/div/a", By.XPATH)
        asserts.fail_if_none(remove_org_link, "Could not find the Remove Org link.")
        remove_org_link.click()

        # Find the Yes button
        yes_button = wait_until_element(self.base.driver, "//button[@type='button']", By.XPATH)
        asserts.fail_if_none(yes_button, "Could not find the Yes button to remove role.")
        yes_button.click()

        # Orgs List link
        org_list_link = wait_until_element(self.base.driver, "//li[@id='org_list']/a", By.XPATH)
        asserts.fail_if_none(org_list_link, "Could not find the Orgs List link.")
        org_list_link.click()

        # Verify that org doesn't exist
        org = wait_until_element(self.base.driver, self._NEW_ORG % name.replace(" ", "_"), By.XPATH)
        asserts.fail_unless_none(org, "Could not delete organization named '%s'." % name)


    def add_env_to_org(self, org_name, prior_env_name, new_env_name):
        """
        Adds a new environment to an existing organization.
        """

        # go to the url
        self.base.driver.get(self.base.base_url)

        # Select the Organizations tab
        self.go_to_organizations_tab()

        # Orgs List link
        org_list_link = wait_until_element(self.base.driver, "//li[@id='org_list']/a", By.XPATH)
        asserts.fail_if_none(org_list_link, "Could not find the Orgs List link.")
        org_list_link.click()

        # Verify that org exists
        org = wait_until_element(self.base.driver, self._NEW_ORG % org_name.replace(" ", "_"), By.XPATH)
        asserts.fail_if_none(org, "Could not locate an organization named '%s'." % org_name)
        org.click()

        # New env should not be found yet
        env = wait_until_element(self.base.driver, "//a[contains(@class, 'subpanel_element')]/div[contains(.,'%s')]" % new_env_name, By.XPATH)
        asserts.fail_unless_none(env, "There is an environment with this name already.")

        # Locate the New Environment button
        new_env_button = wait_until_element(self.base.driver, "//div[contains(@class, 'button subpanel_element')]", By.XPATH)
        asserts.fail_if_none(new_env_button, "Could not find the New Env button.")
        new_env_button.click()

        # Locate the Environment Name field
        env_name_field = wait_until_element(self.base.driver, "//form[@id='new_subpanel']/fieldset/div/input", By.XPATH)
        asserts.fail_if_none(env_name_field, "Could not locate the Environment Name field.")
        env_name_field.send_keys(new_env_name)

        prior_env_list = wait_until_element(self.base.driver, "//form[@id='new_subpanel']/fieldset[3]/div/select", By.XPATH)
        asserts.fail_if_none(prior_env_list, "Could not locate the Previous Environment dropdown.")
        try:
            Select(prior_env_list).select_by_visible_text(prior_env_name)
        except NoSuchElementException, e:
            asserts.fail("Could not locate prior environment named '%s'" % prior_env_name)

        # Locate the Submit button
        submit_button = wait_until_element(self.base.driver, "//form[@id='new_subpanel']/div[2]/input", By.XPATH)
        asserts.fail_if_none(submit_button, "Could not locate the Submit button")
        submit_button.click()


    def delete_env_from_org(self, org_name, env_name):
        """
        Adds a new environment to an existing organization.
        """

        # go to the url
        self.base.driver.get(self.base.base_url)

        # Select the Organizations tab
        self.go_to_organizations_tab()

        # Orgs List link
        org_list_link = wait_until_element(self.base.driver, "//li[@id='org_list']/a", By.XPATH)
        asserts.fail_if_none(org_list_link, "Could not find the Orgs List link.")
        org_list_link.click()

        # Verify that org exists
        org = wait_until_element(self.base.driver, self._NEW_ORG % org_name.replace(" ", "_"), By.XPATH)
        asserts.fail_if_none(org, "Could not locate an organization named '%s'." % org_name)
        org.click()

        # Locate existing env
        env = wait_until_element(self.base.driver, "//a[contains(@class, 'subpanel_element')]/div[contains(.,'%s')]" % env_name, By.XPATH)
        asserts.fail_unless_none(env, "There is an environment with this name already.")
        env.click()

        # Locate the Remove Environment link
        remove_link = wait_until_element(self.base.driver, "//div[@id='subpanel']/div/div[2]/div/a", By.XPATH)
        asserts.fail_if_none(remove_link, "Could not locate the Remove Environment link")
        remove_link.click()

        # Find the Yes button
        yes_button = wait_until_element(self.base.driver, "//button[@type='button']", By.XPATH)
        asserts.fail_if_none(yes_button, "Could not find the Yes button to remove role.")
        yes_button.click()

