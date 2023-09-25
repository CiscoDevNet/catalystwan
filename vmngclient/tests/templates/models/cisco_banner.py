from vmngclient.api.templates.models.cisco_banner_model import CiscoBannerModel

banner_model = CiscoBannerModel(  # type: ignore
    template_name="banner_1", template_description="na", login_banner="login banner", motd_banner="motd_bnanner"
)
