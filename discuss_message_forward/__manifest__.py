# -*- coding: utf-8 -*-
{
    'name': 'Discuss Message Forward',
    'version': '19.0.1.0.0',
    'category': 'Discuss',
    'summary': 'Forward Discuss and chatter messages to other channels or people',
    'description': """
Adds a Forward action to messages in Discuss channels, direct messages,
and record chatter. Forwarding reposts the message - with its
attachments - into one or more other channels and/or as a direct
message to one or more people, with an optional comment.
""",
    'author': 'gamalmouhssine',
    'website': 'https://github.com/gamalmouhssine/discuss-message-forward',
    'support': 'mouhssinegamal2@gmail.com',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/mail_message_forward_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'discuss_message_forward/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
    'price': 2.0,
    'currency': 'EUR',
}
