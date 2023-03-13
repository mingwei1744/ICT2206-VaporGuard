class UserConfig:
    def __init__(self):

        self.resource_naming = ""
        self.vm_dns = ""
        self.vm_rootuser = ""
        self.vm_webuser = ""
        self.web_domain_name = ""
        self.database_key = ""
        self.email = ""
        self.web_codes = ""

    def get_resource_naming(self):
        return self.resource_naming

    def set_resource_naming(self, idata):
        self.resource_naming = idata

    def get_vm_dns(self):
        return self.vm_dns

    def set_vm_dns(self, idata):
        self.vm_dns = idata

    def get_rootuser(self):
        return self.vm_rootuser

    def set_rootuser(self, idata):
        self.vm_rootuser = idata

    def get_webuser(self):
        return self.vm_webuser

    def set_webuser(self, idata):
        self.vm_webuser = idata

    def get_web_domain_name(self):
        return self.web_domain_name

    def set_web_domain_name(self, idata):
        self.web_domain_name = idata

    def get_database_key(self):
        return self.database_key

    def set_database_key(self, idata):
        self.database_key = idata

    def get_email(self):
        return self.email

    def set_email(self, idata):
        self.email = idata

    def get_web_codes(self):
        return self.web_codes

    def set_web_codes(self, idata):
        self.web_codes = idata