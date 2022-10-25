class Repository:

    def __init__(self, session: Session, vmanage_image : str):
        self.session = session
        self.vmanage_image = vmanage_image
    
    def get_image_version(self) -> str:
        
        '''
        The image name in several cases doesn't contain whole image version.
        It's necessary to get the version from vManage which shows whole version.

        @param image: the image name
        '''
        version = ''
        url = '/device/action/software/images?imageType=software'
        image_name = os.path.basename(self.vmanage_image)
        #maby another method
        software_images = self.session.get_data(url)

        for img in software_images:
            if image_name in img['availableFiles']: #string or list, have to check
                version = img['versionName']
                break
        return version