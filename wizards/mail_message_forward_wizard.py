# -*- coding: utf-8 -*-
from markupsafe import Markup

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import format_datetime


class MailMessageForwardWizard(models.TransientModel):
    _name = 'mail.message.forward.wizard'
    _description = 'Forward Message'

    message_id = fields.Many2one('mail.message', string='Message', required=True, readonly=True)
    preview_author = fields.Char(compute='_compute_preview', readonly=True)
    preview_date = fields.Char(compute='_compute_preview', readonly=True)
    preview_body = fields.Html(compute='_compute_preview', readonly=True, sanitize=False)
    channel_ids = fields.Many2many(
        'discuss.channel', string='Channels',
        domain=[('channel_type', '!=', 'chat'), ('is_member', '=', True)],
    )
    partner_ids = fields.Many2many('res.partner', string='People')
    note = fields.Text(string='Comment')

    @api.depends('message_id')
    def _compute_preview(self):
        for wizard in self:
            message = wizard.message_id
            wizard.preview_author = message.author_id.name or message.email_from or _('Someone')
            wizard.preview_date = format_datetime(self.env, message.date) if message.date else ''
            wizard.preview_body = message.body

    def _build_forwarded_body(self):
        """Build the forwarded message body as a quoted block, Telegram/Slack-style.

        Odoo's mail body sanitizer strips CSS classes (``strip_classes=True`` in
        ``mail_thread.py``), so styling has to be inline. Only properties on the
        sanitizer's style whitelist (``odoo/tools/mail.py: _style_whitelist``) are
        used, so the layout survives even if the body is later re-sanitized with
        ``sanitize_style=True`` (e.g. on outgoing email).
        """
        message = self.message_id
        author_name = message.author_id.name or message.email_from or _('Someone')
        date_str = format_datetime(self.env, message.date) if message.date else ''
        forwarded_label = _('Forwarded from')

        header = Markup(
            '<div style="font-size:12px;color:#8a8a8a;margin:8px 0 4px 0;">'
            '↪ %s <strong style="color:#4c4c4c;">%s</strong> '
            '<span style="color:#adadad;">· %s</span>'
            '</div>'
        ) % (forwarded_label, author_name, date_str)

        quote = Markup(
            '<div style="border-left-width:3px;border-left-style:solid;'
            'border-left-color:#c4c4c4;padding:2px 0 2px 12px;margin:0 0 8px 0;">'
            '%s%s</div>'
        ) % (header, message.body or Markup(''))

        if self.note:
            return Markup('<p style="margin:0 0 4px 0;">%s</p>') % self.note + quote
        return quote

    def action_forward(self):
        self.ensure_one()
        if not self.channel_ids and not self.partner_ids:
            raise UserError(_('Select at least one channel or person to forward to.'))

        message = self.message_id
        forwarded_body = self._build_forwarded_body()
        attachment_ids = message.attachment_ids.ids

        for channel in self.channel_ids:
            channel.message_post(
                body=forwarded_body,
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                attachment_ids=attachment_ids,
            )
        for partner in self.partner_ids:
            chat = self.env['discuss.channel']._get_or_create_chat(partners_to=partner.ids)
            chat.message_post(
                body=forwarded_body,
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                attachment_ids=attachment_ids,
            )
        return {'type': 'ir.actions.act_window_close'}
