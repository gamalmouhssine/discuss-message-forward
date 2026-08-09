import { _t } from "@web/core/l10n/translation";
import { registerMessageAction } from "@mail/core/common/message_actions";

registerMessageAction("forward-to-discuss", {
    condition: ({ message }) =>
        message.persistent && ["comment", "email"].includes(message.message_type),
    icon: "fa fa-share-square-o",
    name: ({ thread }) =>
        thread?.model === "discuss.channel" ? _t("Forward") : _t("Forward to Discuss"),
    onSelected: ({ message, owner }) => {
        owner.env.services.action.doAction({
            name: _t("Forward Message"),
            type: "ir.actions.act_window",
            res_model: "mail.message.forward.wizard",
            view_mode: "form",
            views: [[false, "form"]],
            target: "new",
            context: { default_message_id: message.id },
        });
    },
    sequence: 73,
});
