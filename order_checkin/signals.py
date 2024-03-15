# Register your receivers here
from django.db.models import Q, Exists
from django.dispatch import receiver
from django.template.loader import render_to_string

from pretix.base.models import OrderPosition, Order, CheckinList, Checkin
from pretix.control.signals import order_position_buttons


@receiver(order_position_buttons, dispatch_uid="checkin_order_position_buttons")
def order_position_buttons(sender, order: Order, position: OrderPosition, request, **kwargs):
    # Retrieve checkin list from order
    checkin_list = CheckinList.objects.filter(
        Q(
            event=order.event,
            limit_products__in=[position.item_id]
        ) | Q(event=order.event, all_products=True)
    ).first()

    if not checkin_list:
        return

    checked_in = position.checkins.filter(list=checkin_list, successful=True).all()

    # TODO: Handle "checked in but left" case
    if not checked_in.exists():
        return render_to_string("order_checkin/checkin_button.html", {
            "event": order.event,
            "checkinlist": checkin_list,
            "item": position.id,
            "returnquery": f"user={order.code}&item={position.item.id}",
        }, request=request)
    else:
        return render_to_string("order_checkin/checked_out_buttons.html", {
            "event": order.event,
            "checkinlist": checkin_list,
            "item": position.id,
            "returnquery": f"user={order.code}&item={position.item.id}",
        }, request=request)
