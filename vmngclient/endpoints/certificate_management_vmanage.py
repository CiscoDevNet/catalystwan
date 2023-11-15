# mypy: disable-error-code="empty-body"
import datetime

from pydantic.v1 import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get


class WebServerCertificateInfo(BaseModel):
    org_unit: str
    org: str
    location: str
    state: str
    country: str
    company_name: str
    not_before: datetime.datetime = Field(alias="notBefore")
    not_after: datetime.datetime = Field(alias="notAfter")
    certificate_details: str = Field(alias="certificateDetails")
    validity: str


class CertificateManagementVManage(APIEndpoints):
    def dump_certificate(self):
        # GET /setting/configuration/webserver/certificate/certificate
        ...

    def get_certificate(self):
        # GET /setting/configuration/webserver/certificate/getcertificate
        ...

    def get_csr(self):
        # POST /setting/configuration/webserver/certificate
        ...

    def import_certificate(self):
        # PUT /setting/configuration/webserver/certificate
        ...

    def rollback(self):
        # GET /setting/configuration/webserver/certificate/rollback
        ...

    @get("/setting/configuration/webserver/certificate")
    def show_info(self) -> WebServerCertificateInfo:
        ...
