"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           dec-2022

usage:          Django app and Open edX plugin configuration
"""
import logging

from django.apps import AppConfig
from django.conf import settings

from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType

log = logging.getLogger(__name__)


class MobileApiConfig(AppConfig):
    """
    Lawrence McDaniel
    https://lawrencemcdaniel.com

    Configuration class for the Turn The Bus customized mobile_api Django application.
    Spawned from https://github.com/openedx/edx-platform/tree/master/lms/djangoapps/mobile_api
    """

    name = "openedx_plugin_mobile_api"
    verbose_name = "Modified LMS Mobile REST API Endpoint"

    # See: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/edx_django_utils.plugins.html
    plugin_app = {
        # mcdaniel Sep-2021
        # this is how you inject a python list of urls into lms.urls.py
        #
        # The three dict attributes literally equate to the following
        # lines of code being injected into edx-platform/lms/urls.py:
        #
        # import openedx_plugin_api.urls.py
        # url(r"^openedx_plugin/api/", include((urls, "openedx_plugin_api"), namespace="openedx_plugin_api")),
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^openedx_plugin/api/mobile/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },
        # mcdaniel Sep-2021
        # this is how you inject settings into lms.envs.common.py and lms.envs.production.py
        # relative_path == a python module in this repo
        #
        # This dict causes all constants defined in this settings/common.py and settings.production.py
        # to be injected into edx-platform/lms/envs/common.py and edx-platform/lms/envs/production.py
        # Refer to settings/common.py and settings.production.py for example implementation patterns.
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
            },
        },
    }

    def ready(self):
        from .version import __version__
        from .waffle import waffle_switches, is_ready

        log.info("{label} version {version} is ready.".format(label=self.label, version=__version__))
        log.info(
            "{label} {waffle_switches} waffle switches detected.".format(
                label=self.label, waffle_switches=len(waffle_switches.keys())
            )
        )
        if is_ready():
            for switch in waffle_switches:
                if waffle_switches[switch]:
                    log.info("WaffleSwitch {switch} is enabled.".format(switch=switch))
                else:
                    log.warning("WaffleSwitch {switch} is not enabled.".format(switch=switch))