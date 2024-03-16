# Register your receivers here
from django.db.models import Q
from django.dispatch import receiver
from django.template.loader import render_to_string

from pretix.base.models import OrderPosition, Order, CheckinList, Checkin
from pretix.control.signals import order_position_buttons


@receiver(order_position_buttons, dispatch_uid="checkin_order_position_buttons")
def order_position_buttons(
    sender, order: Order, position: OrderPosition, request, **kwargs
):
    # Retrieve checkin list from order
    checkin_list = CheckinList.objects.filter(
        Q(event=order.event, limit_products__in=[position.item_id])
        | Q(event=order.event, all_products=True)
    ).first()

    if not checkin_list:
        return

    output_html = ""

    checkins = position.checkins.filter(list=checkin_list, successful=True).order_by(
        "-datetime"
    )
    has_left = (
        False if not checkins.exists() else checkins.first().type == Checkin.TYPE_EXIT
    )

    template_ctx = {
        "event": order.event,
        "checkinlist": checkin_list,
        "item": position.id,
        "returnquery": f"user={order.code}&item={position.item.id}",
    }

    if has_left or not checkins.exists():
        output_html += render_to_string(
            "pretix_order_checkin/check_in_button.html", template_ctx, request=request
        )

    if checkins.exists():
        if not has_left:
            output_html += render_to_string(
                "pretix_order_checkin/check_out_button.html",
                template_ctx,
                request=request,
            )
        output_html += render_to_string(
            "pretix_order_checkin/delete_check_in_button.html",
            template_ctx,
            request=request,
        )

    return output_html
