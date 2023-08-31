from vmngclient.endpoints import APIEndpoints, post
from vmngclient.utils.upgrades_helper import SoftwarePackageUpdatePayload


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
    def install_pkg(self, payload: SoftwarePackageUpdatePayload) -> None:
        ...

    def process_software_image(self):
        # POST /device/action/software/package/{imageType}
        ...
