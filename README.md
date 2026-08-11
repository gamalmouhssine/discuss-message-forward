# Discuss Message Forward

Odoo 19 addon that adds a **Forward** action to messages in Discuss channels, direct
messages, and record chatter.

Forwarding reposts the message — including its attachments — into one or more other
channels and/or as a direct message to one or more people, with an optional comment.
If a person doesn't already have a direct-message chat with you, one is created
automatically, the same as starting a new chat from Discuss.

## Where it appears

- **Discuss channels & direct messages**: hover a message, click **Forward** in the
  action toolbar.
- **Chatter** (messages logged on any record, e.g. a Sales Order): hover a message,
  click **Forward to Discuss**. This sits alongside Odoo's built-in **Forward** action
  (which opens the full email composer to forward via email) — the two are independent
  and don't conflict.

Both open the same wizard: a preview of the original message, pickers for target
channels and/or people, an optional comment field, and a **Forward** button.

## How it works

- Posting into channels/DMs reuses Odoo's own `discuss.channel.message_post` and the
  same `_get_or_create_chat` helper Discuss's own "new chat" flow uses — so forwarding
  respects normal channel membership and access rules. You can only forward into
  channels/DMs you're already part of or allowed to join; no separate permission model
  is introduced.
- The forwarded message is a plain `mail.message` recording the original author and
  date, followed by the original body, styled as a quoted block. Attachments are
  many2many-linked onto the new message (not copied), so the original message keeps
  its attachments untouched.

## Installation

1. Drop the `discuss_message_forward/` folder into an addons path that also has the
   `mail` module available (any standard Odoo 19 install).
2. Update the app list and install **Discuss Message Forward** from Apps.

Depends only on `mail` — no other modules required.

## Structure

```
discuss_message_forward/
  __manifest__.py
  security/ir.model.access.csv               # access rights for the forward wizard
  wizards/mail_message_forward_wizard.py      # wizard model + forwarding logic
  wizards/mail_message_forward_wizard_views.xml
  static/src/js/message_actions.js            # registers the Forward action in the
                                               # Discuss message-actions registry
```

## License

OPL-1 (Odoo Proprietary License v1.0)
