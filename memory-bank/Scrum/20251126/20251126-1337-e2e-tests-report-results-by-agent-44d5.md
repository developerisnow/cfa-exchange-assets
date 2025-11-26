---
created: 2025-11-26 13:37
updated: 2025-11-26 13:37
type: testing-report
sphere: exchange
topic: e2e-playwright-localhost
author: Alex
agentID: codex-cli-co-76ca
partAgentID: [co-76ca]
version: 1.0.0
tags: [localhost, playwright, keycloak, e2e, smoke]
---

Контекст: запуск `USE_KEYCLOAK_AUTH=true make e2e` на eywa1, локальный стек (gateway 55000, portals 3001/3002/3003, Keycloak 58080). Playwright=да везде.

| e2e-title | playwright | filename | status | Description | Comment |
|-----------|------------|----------|--------|-------------|---------|
| swagger availability - gateway | yes | tests/swagger-availability.spec.ts | work | /swagger/index.html доступен | 200 OK |
| swagger availability - identity | yes | tests/swagger-all-services.spec.ts | work | Identity swagger доступен | 200 OK |
| swagger availability - issuance | yes | tests/swagger-all-services.spec.ts | work | Issuance swagger доступен | 200 OK |
| swagger availability - registry | yes | tests/swagger-all-services.spec.ts | work | Registry swagger доступен | 200 OK |
| swagger availability - settlement | yes | tests/swagger-all-services.spec.ts | work | Settlement swagger доступен | 200 OK |
| swagger availability - compliance | yes | tests/swagger-all-services.spec.ts | work | Compliance swagger доступен | 200 OK |
| investor self-registration verifies email and logs in | yes | tests/self-registration.spec.ts | work | Поток саморегистрации инвестора завершился | локальный стек |
| backoffice admin authenticates via Keycloak | yes | tests/backoffice-auth.spec.ts | notWork | Не дождались заголовка «Дашборд» | Страница остаётся на mock-логине, KC форма не показалась |
| backoffice audit page renders and filters | yes | tests/backoffice-audit.spec.ts | notWork | Не дождались заголовка «Дашборд» | Логин не прошёл через KC |
| backoffice KYC page renders | yes | tests/backoffice-kyc.spec.ts | notWork | Не дождались заголовка «Дашборд» | Логин не прошёл через KC |
| issuer payout schedule stub shows empty then adds item | yes | tests/issuer-payout-schedule.spec.ts | notWork | Не дождались «Главная/Dashboard» | Зависли на странице логина (mock) |
| issuer dashboard renders KPIs | yes | tests/issuer-reports.spec.ts | notWork | Не дождались «Главная/Dashboard» | Зависли на странице логина (mock) |
| issuer reports page shows table or empty state | yes | tests/issuer-reports.spec.ts | notWork | Не дождались «Главная/Dashboard» | Зависли на странице логина (mock) |
| issuer portal authenticates via Keycloak | yes | tests/public-auth.spec.ts | notWork | Не дождались перехода на /dashboard | Кнопка KC нажата, но остались на mock-логине |
| investor portal authenticates via Keycloak | yes | tests/public-auth.spec.ts | notWork | Strict-mode violation (2 кнопки «Войти») | Нужно выбирать KC кнопку и дожидаться KC формы |
| swagger availability - gateway (duplicate aggregate) | yes | tests/swagger-all-services.spec.ts | work | Итог в агрегированном наборе | Входит в общий smoke |
