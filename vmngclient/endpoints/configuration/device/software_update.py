# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, post
from vmngclient.utils.upgrades_helper import SoftwarePackageUploadPayload


class ConfigurationDeviceSoftwareUpdate(APIEndpoints):
    def download_package_file(self):
        # GET /device/action/software/package/{fileName}
        ...

    def edit_image_metadata(self):
        # PUT /device/action/software/package/{versionId}/metadata
        ...

    def get_image_metadata(self):
        # GET /device/action/software/package/{versionId}/metadata
        ...

    def get_upload_images_count(self):
        # GET /device/action/software/package/imageCount
        ...

    @post("/device/action/software/package")
    def upload_software_to_manager(self, payload: SoftwarePackageUploadPayload) -> None:
        ...

    def process_software_image(self):
        # POST /device/action/software/package/{imageType}
        ...
