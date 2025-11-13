 Шаги

  1. Проверил Wrangler и токен

  - wrangler 4.47.0 установлен.
  - Token verify: active.
  - whoami показывает ваш аккаунт и права (без секретов).

  2. Получил Account ID из API

  - Account ID: eb5f5a59c555cd08c2518c8cf22d6aa6
  - Рекомендую добавить в .env: CLOUDFLARE_ACCOUNT_ID=eb5f5a59c555cd08c2518c8cf22d6aa6
    Команда (ничего не выводит секретов):
    echo 'CLOUDFLARE_ACCOUNT_ID=eb5f5a59c555cd08c2518c8cf22d6aa6' >> /home/user/__Repositories/cloudflare__developerisnow/.env

  3. Headless-аутентификация для Wrangler

  - Wrangler автоматически берёт токен из CLOUDFLARE_API_TOKEN и Account ID из CLOUDFLARE_ACCOUNT_ID.
  - Примеры:
      - Список Pages проектов: wrangler pages project list --account-id $CLOUDFLARE_ACCOUNT_ID
      - Создать Pages проект: wrangler pages project create <name> --production-branch main --account-id $CLOUDFLARE_ACCOUNT_ID
      - Деплой Pages: wrangler pages deploy dist --project-name <name>
      - Workers/KV/D1/R2 командами Wrangler по месту.

  4. Поставил flarectl (CLI к Cloudflare API)

  - Установлено через go install; доступен flarectl -v (dev).
  - Использование (через Token, без email/pass): CF_API_TOKEN=$CLOUDFLARE_API_TOKEN flarectl zone list
  - Примеры:
      - DNS записи: CF_API_TOKEN=... flarectl dns list --zone example.com
      - Purge cache: CF_API_TOKEN=... flarectl zone purge --zone example.com --everything

  5. cloudflared (опционально, для Tunnels)

  - Установка из GitHub/apt у нас упёрлась во внешний таймаут. Готов докрутить позже.
  - Рекомендовано, если нужны Argo Tunnel/Quick Tunnels. Иначе можно не ставить.

  Сравнение (кратко)

  - Wrangler: Workers + Pages + KV/D1/R2; Dev Platform; Auth: CLOUDFLARE_API_TOKEN (+ CLOUDFLARE_ACCOUNT_ID).
  - flarectl: Общий API (DNS/Zones/Cache/Firewall и т.д.); Быстрые операции без кода; Auth: CF_API_TOKEN или CF_API_KEY+CF_API_EMAIL.
  - cloudflared: Tunnels (Argo/Quick); Локалка→Cloudflare; Auth: browser login или cert/token.
  - Terraform (опция): IaC для всего Cloudflare; стабильная декларативка; Auth: API Token.

