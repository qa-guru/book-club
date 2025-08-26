import { Fixtures } from '@playwright/test';
import { PlaywrightHomePage } from '../pages/playwright-home-page';
import { ContextPagesFixture } from './context-pages';

export type PlaywrightPagesFixture = {
  playwrightHomePage: PlaywrightHomePage;
};

export const playwrightPagesFixture: Fixtures<PlaywrightPagesFixture, ContextPagesFixture> = {
  playwrightHomePage: async ({ contextPage }, use) => {
    const playwrightHomePage = new PlaywrightHomePage(contextPage);

    await use(playwrightHomePage);
  },
};
