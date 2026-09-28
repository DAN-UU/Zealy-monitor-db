# Zealy Monitor

Monitors a Zealy community for genuinely new **published quests** and sends Telegram alerts.

## Detection architecture

```text
Zealy API → extract published quest IDs → compare with persistent state → Telegram
```

The monitor does **not** treat a changed page/API response as a new quest. A quest is new only when its stable Zealy `id` has not been seen before.

### First run
The first successful check creates a baseline from the quests that already exist. It sends **no alerts** for those existing quests.

### API safety
A failed request, invalid response, or suspicious empty quest list does not overwrite the saved state.

## Persistent storage on Vercel

For Vercel/serverless use, configure an Upstash Redis integration and provide:

```text
KV_REST_API_URL
KV_REST_API_TOKEN
```

The monitor automatically uses these variables. The local `seen_items.json` file is only a development fallback and should not be relied on for a serverless deployment.

Optional:

```text
ZEALY_STATE_KEY=zealy-monitor:state
```

## Environment variables

```text
ZEALY_SUBDOMAIN=your-community-subdomain
ZEALY_API_KEY=your-zealy-api-key
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
POLL_INTERVAL=60
KV_REST_API_URL=your-upstash-rest-url
KV_REST_API_TOKEN=your-upstash-rest-token
```

## Webhooks

Zealy webhooks are push events sent to an HTTPS endpoint. They are useful for events such as `SPRINT_STARTED`, `SPRINT_ENDED`, and quest claim events. Zealy's documented webhook event list does **not** include a `QUEST_PUBLISHED` event, so this monitor still uses the Zealy quest API to detect newly published quests.

Do not run both a polling quest alert and a second quest alert integration unless you intentionally want duplicate messages.
