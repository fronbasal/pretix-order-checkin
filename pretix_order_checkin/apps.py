from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_order_checkin"
    verbose_name = "Pretix Check-in button on Order Page"

    class PretixPluginMeta:
        name = gettext_lazy("Pretix Check-in button on Order Page")
        author = "Daniel Malik"
        description = gettext_lazy("Add a check-in button to the order detail and overview page")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA
