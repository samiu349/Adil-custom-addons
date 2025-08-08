from odoo import models, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        order = super().create(vals)

        # Récupère tous les utilisateurs du groupe approbateur
        group = self.env.ref('alt_larmouss_custom.group_purchase_approver', raise_if_not_found=False)
        if group:
            partners = group.users.mapped('partner_id')

            # 🔔 Notification système
            order.message_post(
                body=_("Un nouveau bon de commande a été créé : %s") % order.name,
                partner_ids=partners.ids
            )

            # 📧 Notification email
            template = self.env.ref('alt_larmouss_custom.email_notification_paynow', raise_if_not_found=False)
            if template:
                for user in self.env.ref('alt_larmouss_custom.group_purchase_approver').users:
                    if user.partner_id.email:
                        template.send_mail(
                            self.id,
                            force_send=True,
                            email_values={'partner_ids': [(6, 0, [user.partner_id.id])]}
                        )

        return order
