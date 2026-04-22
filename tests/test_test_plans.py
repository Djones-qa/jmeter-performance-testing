"""
Tests for JMeter test plan files existence and structure.
"""
import pytest
import os
import xml.etree.ElementTree as ET


class TestTestPlans:

    def test_smoke_test_plan_exists(self):
        assert os.path.exists("test-plans/smoke-test.jmx"), \
            "smoke-test.jmx not found"

    def test_load_test_plan_exists(self):
        assert os.path.exists("test-plans/load-test.jmx"), \
            "load-test.jmx not found"

    def test_smoke_test_is_valid_xml(self):
        tree = ET.parse("test-plans/smoke-test.jmx")
        root = tree.getroot()
        assert root.tag == "jmeterTestPlan"

    def test_load_test_is_valid_xml(self):
        tree = ET.parse("test-plans/load-test.jmx")
        root = tree.getroot()
        assert root.tag == "jmeterTestPlan"

    def test_smoke_test_has_thread_group(self):
        tree = ET.parse("test-plans/smoke-test.jmx")
        root = tree.getroot()
        xml_str = ET.tostring(root, encoding="unicode")
        assert "ThreadGroup" in xml_str

    def test_load_test_has_thread_group(self):
        tree = ET.parse("test-plans/load-test.jmx")
        root = tree.getroot()
        xml_str = ET.tostring(root, encoding="unicode")
        assert "ThreadGroup" in xml_str

    def test_smoke_test_has_http_sampler(self):
        tree = ET.parse("test-plans/smoke-test.jmx")
        xml_str = ET.tostring(tree.getroot(), encoding="unicode")
        assert "HTTPSamplerProxy" in xml_str

    def test_load_test_has_assertions(self):
        tree = ET.parse("test-plans/load-test.jmx")
        xml_str = ET.tostring(tree.getroot(), encoding="unicode")
        assert "ResponseAssertion" in xml_str

    def test_smoke_test_targets_httpbin(self):
        tree = ET.parse("test-plans/smoke-test.jmx")
        xml_str = ET.tostring(tree.getroot(), encoding="unicode")
        assert "httpbin.org" in xml_str

    def test_load_test_has_50_threads(self):
        tree = ET.parse("test-plans/load-test.jmx")
        xml_str = ET.tostring(tree.getroot(), encoding="unicode")
        assert "50" in xml_str
