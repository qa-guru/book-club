import { expect } from '@playwright/test';
import { loginTest as test } from './tests';

test.beforeEach(async ({ playwrightHomePage }) => {
  await playwrightHomePage.visit('/signin');
});

test('login with invalid password', async ({ playwrightHomePage }) => {
  await playwrightHomePage.loginForm.enterUsername('alex')
  await playwrightHomePage.loginForm.enterPassword('None')
  await playwrightHomePage.loginForm.clickOnSubmitButton()
  await playwrightHomePage.loginForm.errorMessageShouldHaveText('Ты не пройдешь!')
  await expect(playwrightHomePage.page.getByTestId('error-message')).toHaveText('Ты не пройдешь!')
});
