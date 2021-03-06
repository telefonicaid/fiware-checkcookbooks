# coding=utf-8
from django.test import TestCase
from recipes.productrequest import *
from recipes import kingstion, loggers, productrelease
from mockito import *
from mock import MagicMock
import json
import xml.etree.ElementTree


class ProductRequestTest(TestCase):
    def setUp(self):
        self.product_list = {"product": [
            {"name": "tomcat", "description": "tomcat J2EE container",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "nodejs", "description": "nodejs",
             "attributes": {"key": "aux", "value": "aux",
                            "description": "aux"},
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "mysql", "description": "mysql",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "git", "description": "git",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "mongodbshard", "description": "mongodbshard",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "mongos", "description": "mongos",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "mongodbconfig", "description": "mongodbconfig",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "contextbroker", "description": "contextbroker",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "postgresql", "description": "db manager", "attributes": [
                {"key": "username", "value": "postgres",
                 "description": "The administrator usename"},
                {"key": "password", "value": "postgres",
                 "description": "The administrator password"}],
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "haproxy", "description": "balancer",
             "attributes": {"key": "sdccoregroupid",
                            "value": "app_server_role",
                            "description": "idcoregroup"},
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "test", "description": "test",
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "testPuppet", "description": "testPuppet",
             "metadatas": {"key": "installator", "value": "puppet",
                           "description": "Puppet Manifest required"}},
            {"name": "mediawiki", "description": "MediaWiki Product",
             "attributes": [{"key": "wikiname", "value": "Wiki to be shown",
                             "description": "The name of the wiki"},
                            {"key": "path", "value": "/demo",
                             "description":
                                 "The url context to be displayed"}],
             "metadatas": {"key": "installator", "value": "chef",
                           "description": "ChefServer Recipe required"}},
            {"name": "beatest", "description": "Last test of server TESTER",
             "attributes": [{"key": "name1", "value": "value1"},
                            {"key": "name2", "value": "value2"}],
             "metadatas": [{"key": "image",
                            "value": "12c2726c-17b5-401f-9dc7-48a351a8fc64"},
                           {"key": "cookbook_url",
                            "value":
                                "https://forge.fi-ware.org/scmrepos/svn/"
                                "testbed/trunk/cookbooks/GESoftware/beatest/"},
                           {"key": "cloud", "value": "yes"},
                           {"key": "installator", "value": "chef"},
                           {"key": "open_ports", "value": "22 port1 port2"},
                           {"key": "repository", "value": "svn"},
                           {"key": "public", "value": "no"},
                           {"key": "tenant_id",
                            "value": "376f0169d04b4a66a1af147ef33073ae"},
                           {"key": "dependencies", "value": "git"}]},
            {"name": "", "description": "Product only for test", "metadatas": [
                {"key": "image",
                 "value": "df44f62d-9d66-4dc5-b084-2d6c7bc4cfe4"},
                {"key": "cookbook_url", "value": ""},
                {"key": "cloud", "value": "yes"},
                {"key": "installator", "value": "chef"},
                {"key": "open_ports", "value": "80 22"}]}]}
        self.product = {"name": "beatest",
                        "description": "Last test of server TESTER",
                        "attributes": [{"key": "name1", "value": "value1"},
                                       {"key": "name2", "value": "value2"}],
                        "metadatas": [{"key": "image",
                                       "value": "12c2726c-17b5-401f-9dc7-48a351a8fc64"},
                                      {"key": "cookbook_url",
                                       "value": "https://forge.fi-ware.org/scmrepos/svn/testbed/trunk/cookbooks/GESoftware/beatest/"},
                                      {"key": "cloud", "value": "yes"},
                                      {"key": "installator", "value": "chef"},
                                      {"key": "open_ports",
                                       "value": "22 port1 port2"},
                                      {"key": "repository", "value": "svn"},
                                      {"key": "public", "value": "no"},
                                      {"key": "tenant_id",
                                       "value":
                                           "376f0169d04b4a66a1af147ef33073ae"},
                                      {"key": "dependencies", "value": "git"}]}
        self.token = "token"
        self.tenant = "tenantId"
        self.name = "beatest"
        self.version = "2.0"
        when(kingstion).get_sdc().thenReturn("sdc_url")
        when(kingstion).get_keystone().thenReturn("kingston_url")
        self.product_request = ProductRequest(self.token, self.tenant)
        msg = mock()
        when(loggers).set_info_log(msg).thenReturn(None)
        when(loggers).set_error_log(msg).thenReturn(None)

    def test_delete_product_with_version(self):
        response_delete_with = mock()
        when(ProductReleaseRequest).get_product_release(self.name).thenReturn(
            self.version)
        when(ProductReleaseRequest). \
            delete_product_release(self.name, self.version).thenReturn(None)
        when(http).delete(any(), self.product_request.header).thenReturn(
            response_delete_with)
        when(response_delete_with).status().thenReturn(200)
        result = self.product_request.delete_product(self.name)
        self.assertIsNone(result)
        self.assertEqual(result, None)

    def test_delete_product_without_version(self):
        response_delete = mock()
        when(ProductReleaseRequest).get_product_release(self.name).thenReturn(
            self.version)
        when(http).delete(any(), self.product_request.header).thenReturn(
            response_delete)
        when(ProductReleaseRequest). \
            delete_product_release(self.name, self.version).thenReturn(None)
        when(response_delete).status().thenReturn(200)
        result = self.product_request.delete_product(self.name)
        self.assertEqual(result, None)

    def test_get_products(self):
        response_get = mock()
        when(ProductReleaseRequest).get_product_release(self.name).thenReturn(
            self.version)
        when(http).get(any(), self.product_request.header).thenReturn(
            response_get)
        when(response_get).status().thenReturn(200)
        when(json).loads(response_get.read()).thenReturn(self.product_list)
        result, products = self.product_request.get_products()
        self.assertEqual(result, None)

    def test_get_product_info(self):
        response_get_info = mock()
        when(ProductReleaseRequest).get_product_release(self.name).thenReturn(
            self.version)
        when(http).get(any(), self.product_request.header).thenReturn(
            response_get_info)
        when(response_get_info).status().thenReturn(200)
        when(json).loads(response_get_info.read()).thenReturn(self.product)
        result = self.product_request.get_product_info(self.name)
        self.assertEqual(result, "Last test of server TESTER")

    def test_add_product(self):
        response_add = mock()
        product_mocked = mock()
        attributes = mock()
        attributes_list = MagicMock()
        metadatas = mock()
        metadatas_list = MagicMock()
        payload = mock()
        paylaod_string = mock()
        when(productrelease).Product(self.name, "description").thenReturn(
            product_mocked)
        when(productrelease).process_attributes(attributes).thenReturn(
            iter(attributes_list))
        when(product_mocked).add_attribute(any()).thenReturn(None)
        when(productrelease).process_attributes(metadatas).thenReturn(
            iter(metadatas_list))
        when(product_mocked).add_metadata(any()).thenReturn(None)
        when(product_mocked).to_product_xml().thenReturn(payload)
        when(xml.etree.ElementTree).tostring(payload). \
            thenReturn(paylaod_string)
        when(http).post(any(), self.product_request.header2, any()).thenReturn(
            response_add)
        when(response_add).status().thenReturn(200)
        result_error, product = self.product_request.add_product(self.name,
                                                                 "description",
                                                                 attributes,
                                                                 metadatas)
        self.assertIsNone(result_error)
        self.assertIsNotNone(product)


class Attributes(TestCase):
    def test_process_attributes_description(self):
        attributes_string = "key=value,description"
        attribute = ["key", "value", "description"]
        when(productrelease).Attribute(any(), any(), any()).thenReturn(
            attribute)
        result = productrelease.process_attributes(attributes_string)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 3)

    def test_process_attributes_no_attribute(self):
        attributes_string = None
        attribute = mock()
        when(productrelease).Attribute(any(), any(), any()).thenReturn(
            attribute)
        result = productrelease.process_attributes(attributes_string)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_process_attributes_no_description(self):
        attributes_string = "key=value,description"
        attribute = mock()
        when(productrelease).Attribute(any(), any(), any()).thenReturn(
            attribute)
        result = productrelease.process_attributes(attributes_string)
        self.assertEqual(len(result), 1)


class ProductRequestReleaseTest(TestCase):
    def setUp(self):
        self.product = {"productRelease":
                            {"version": "2.4.10",
                             "product": {"name": "beatest",
                                         "description":
                                             "Last test of server TESTER",
                                         "attributes": [
                                             {"key": "name1",
                                              "value": "value1"},
                                             {"key": "name2",
                                              "value": "value2"}],
                                         "metadatas": [
                                             {"key": "image",
                                              "value":
                                                  "12c2726c-17b5-401f-9dc7-"
                                                  "48a351a8fc64"},
                                             {
                                                 "key": "cookbook_url",
                                                 "value":
                                                     "https://forge.fi-ware."
                                                     "org/scmrepos/svn/testbed"
                                                     "/trunk/cookbooks/"
                                                     "GESoftware/beatest/"},
                                             {"key": "cloud",
                                              "value": "yes"}, {
                                                 "key": "installator",
                                                 "value": "chef"},
                                             {
                                                 "key": "open_ports",
                                                 "value": "22 port1 port2"},
                                             {
                                                 "key": "repository",
                                                 "value": "svn"},
                                             {"key": "public",
                                              "value": "no"},
                                             {"key": "tenant_id",
                                              "value":
                                                  "376f0169d04b4a6"
                                                  "6a1af147ef33073ae"},
                                             {
                                                 "key": "dependencies",
                                                 "value": "git"}]}}}
        self.token = "token"
        self.tenant = "tenantId"
        self.name = "beatest"
        self.version = "2.0"
        self.products = []
        when(kingstion).get_sdc().thenReturn("sdc_url")
        when(kingstion).get_keystone().thenReturn("kingston_url")
        self.product_request_release = ProductReleaseRequest(self.token,
                                                             self.tenant)
        msg = mock()
        when(loggers).set_info_log(msg).thenReturn(None)
        when(loggers).set_error_log(msg).thenReturn(None)

    def test_get_product_release_info(self):
        response_get_info = mock()
        when(http).get(any(), self.product_request_release.header).thenReturn(
            response_get_info)
        when(response_get_info).status().thenReturn(200)
        when(json).loads(response_get_info.read()).thenReturn(self.product)
        result = self.product_request_release.get_product_release_info(
            self.name, self.version)
        self.assertEqual(result, "Last test of server TESTER")

    def test_get_product_release(self):
        response_get = mock()
        when(http).get(any(), self.product_request_release.header).thenReturn(
            response_get)
        when(response_get).status().thenReturn(200)
        when(json).loads(response_get.read()).thenReturn(self.product)
        result = self.product_request_release.get_product_release(self.name)
        self.assertEqual(result, "2.4.10")

    def test_delete_product_release(self):
        response_delete = mock()
        when(http).delete(
            any(), self.product_request_release.header). \
            thenReturn(response_delete)
        when(ProductReleaseRequest). \
            delete_product_release(self.name, self.version).thenReturn(None)
        when(response_delete).status().thenReturn(200)
        result = self.product_request_release. \
            delete_product_release(self.name, self.version)
        self.assertEqual(result, None)

    def test_add_product_release(self):
        product = mock()
        payload = mock()
        paylaod_string = mock()
        product_mocked = mock()
        when(productrelease).ProductRelease(product, self.version).thenReturn(
            product_mocked)
        when(product_mocked).to_product_xml().thenReturn(payload)
        when(xml.etree.ElementTree).tostring(payload).thenReturn(
            paylaod_string)
        response_add = mock()
        when(http).post(any(), self.product_request_release.header2,
                        any()).thenReturn(response_add)
        when(response_add).status().thenReturn(200)
        result_add = self. \
            product_request_release. \
            add_product_release(product, self.name, self.version)
        self.assertEqual(result_add, None)
