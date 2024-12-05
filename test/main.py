import unittest
import logging
from time import sleep
import requests
import docker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)-8s %(message)s"
)

class TestExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.info("Setting up client connection")
        cls.client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        logging.info("Client connected")

    def test_addition(self):
        logging.info("Testing addition")
        logging.info("2 + 2 = 4")
        self.assertEqual(2 + 2, 4)

    def test_no_access_to_random_path(self):
        logging.info("Testing no access to random path")
        response = requests.get('http://necroginx:80/test-container')
        status_code = response.status_code
        logging.info(f'http://necroginx:80/test-container statusCode: {status_code}')
        self.assertEqual(status_code, 404)

    def test_start_necroginx_capable_container(self):
        logging.info("Testing access to necroginx capable container")
        self.nginx_container = self.client.containers.run(
            "nginx:latest",
            detach=True,
            network="test_my-network",
            environment={
                "NECROGINX_ROUTE":"my-service",
                "NECROGINX_PORT":"80"
            }
        )

        sleep(2)

        logging.info("Testing is the path opened")
        response = requests.get('http://necroginx:80/my-service')
        status_code = response.status_code
        logging.info(f'http://necroginx:80/my-service statusCode: {status_code}')
        self.assertEqual(status_code, 200)

        self.nginx_container.stop()
        self.nginx_container.remove()

        sleep(5)

        logging.info("Testing is the path closed")
        response = requests.get('http://necroginx:80/my-service')
        status_code = response.status_code
        logging.info(f'http://necroginx:80/my-service statusCode: {status_code}')
        self.assertEqual(status_code, 404)

    @classmethod
    def tearDownClass(cls):
        logging.info("Tearing down client connection")


if __name__ == '__main__':
    logging.info("Starting tests")
    unittest.main()