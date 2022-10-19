from vmngclient.session import Session


class SDAVC:
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def enable(self):
        endpoint = '/dataservice/clusterManagement/setup/'
        payload = {"vmanageID":"0","deviceIP":"10.0.1.200","username":"admin","password":"Cisco#123@Viptela","persona":"COMPUTE_AND_DATA","services":{"sd-avc":{"server":True}}}
        endpoint = '/dataservice/clusterManagement/setup/'
        import requests
        response = requests.put(url=self.session.get_full_url(endpoint),
                     headers=self.session.session_headers,
                     json=payload,
                     verify=False)
        # response = self.session.relogin_request("PUT", endpoint, payload)
        return response
        
    def disable(self):
        payload = {"vmanageID":"0",
            "deviceIP":"10.0.1.200",
            "username":"admin",
            "password":"Cisco#123@Viptela",
            "persona":"COMPUTE_AND_DATA",
            "services":
                {
                    "sd-avc":
                        {
                            "server": False
                        }
                }
            }
        endpoint = '/dataservice/clusterManagement/setup/'
        response = self.session.relogin_request("PUT", endpoint, payload)
        return response