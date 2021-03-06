# coding=utf-8
from recipes import kingstion, productrequest


class Catalog:
    def __init__(self, name, version, desc, token):
        """
        Initial parameters
        @param name: of the product/software
        @param version: version of the product / software
        @param desc: description of the product/software
        @param token: token
        """
        self.name = name
        self.version = version
        self.attr = None
        self.desc = desc
        self.meta = None
        self.token = token
        self.tenant = kingstion.get_tenant_from_token(token)

    def set_attributes(self, attr):
        """
        Set attributes of the product
        @param attr: attributes
        @return: the attributes
        """
        self.attr = attr
        return attr

    def get_metadata(self, manager, uri, sos, depend, tcp, udp, repo, token):
        """
        Create a string with all the metadatas
        @param manager: software management type
        @param uri: url of the software repository
        @param sos: images id
        @param depend: software dependencies
        @param tcp: tcp ports
        @param udp: udp ports
        @param repo: type of repository (git or svn)
        @param token: token
        @return: the string with the metadata
        """
        meta = "installator=" + manager
        if tcp == "":
            meta += ";open_ports=22"
        else:
            meta += ";open_ports=22 " + tcp
        meta += ";cloud=yes"
        meta += ";open_ports_udp=" + udp
        meta += ";repository=" + repo
        meta += ";public=no"
        meta += ";cookbook_url=" + uri
        meta += ";tenant_id=" + kingstion.get_tenant_from_token(token)
        images = ""
        #Ya cambiado para que se pase el id
        for so in sos:
            if images != "":
                images += " " + so
            else:
                images = so
        meta += ";image=" + images

        if depend is not None:
            meta += ";" + depend
        self.meta = meta
        return meta

    def remove_catalog(self):
        """
        Remove a software from the catalog
        @return: None if all OK or an error on failure
        """
        try:
            g = productrequest.ProductRequest(self.token, self.tenant)
            gr = productrequest.ProductReleaseRequest(self.token, self.tenant)
            err = gr.delete_product_release(self.name, self.version)
            if err is not None:
                return 'Error deleting the product release'
            err = g.delete_product(self.name)
            if err is not None:
                return "Error deleting the product "
        except Exception:
            msg = "Error delete the recipes to SDC server"
            return msg

        return None

    def add_catalog(self):
        """
        Add a software to the catalog
        @return: None if all OK or an error on failure
        """
        try:
            g = productrequest.ProductRequest(self.token, self.tenant)
            gr = productrequest.ProductReleaseRequest(self.token, self.tenant)
            err, product = g.add_product(self.name, self.desc, self.attr, self.meta)
            if err is not None:
                return "Error adding the product"
            err = gr.add_product_release(product, self.name, self.version)
            if err is not None:
                return "Error adding the product release"
        except Exception:
            msg = "Error updating the recipes to SDC server"
            return msg
        return None


def process_data(data):
    """
    Remove characters from a string
    @param data: the string
    @return: the modified string
    """
    return " ".join(
        " ".join(" ".join(
            " ".join(" ".join(
                " ".join(data.split(
                    ",")).split(";")).split(
                "-")).split("    ")).split(
            "   ")).split("  "))
