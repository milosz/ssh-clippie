import errno
import io
import unittest.mock
from unittest import TestCase

import utils


class Test(TestCase):
    def test_set_verbose_mode(self):
        # verbose mode
        utils.set_verbose_mode("verbose")
        self.assertTrue(utils.output.get_verbose_mode())

        # quiet mode
        utils.set_verbose_mode("quiet")
        self.assertFalse(utils.output.get_verbose_mode())

    def test_set_ssh_directory(self):
        # custom
        ssh_directory = "/home/user/.ssh"
        utils.set_ssh_directory(ssh_directory)
        self.assertEqual(utils.directory.get_ssh_directory(), ssh_directory)

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_message_verbose(self, mock_stdout):
        message = "Hello World!"
        utils.set_verbose_mode("verbose")
        utils.output.print_message(message)
        self.assertEqual(mock_stdout.getvalue(), f"{message}\n")

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_message_quiet(self, mock_stdout):
        message = "Hello World!"
        utils.set_verbose_mode("quiet")
        utils.output.print_message(message)
        self.assertEqual(mock_stdout.getvalue(), "")

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_header_verbose(self, mock_stdout):
        message = "Hello World!"
        utils.set_verbose_mode("verbose")
        utils.output.print_header(message)
        self.assertEqual(mock_stdout.getvalue(), f"{message}\n")

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_header_quiet(self, mock_stdout):
        message = "Hello World!"
        utils.set_verbose_mode("quiet")
        utils.output.print_header(message)
        self.assertEqual(mock_stdout.getvalue(), "")

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_error_message(self, mock_stdout):
        file_type = "directory"
        file_path = "/home/user/.ssh"
        sub_message = "empty"
        message = "should not exist"

        utils.output.print_error_message(file_type, file_path, sub_message, message)
        self.assertEqual(
            mock_stdout.getvalue(),
            f"{file_type} {file_path} ({sub_message}) {message}\n",
        )

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_error_message_with_fix(self, mock_stdout):
        file_type = "directory"
        file_path = "/home/user/.ssh"
        current_value = "700"
        expected_value = "600"

        utils.output.print_error_message_with_fix(
            file_type, file_path, current_value, expected_value
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            f"{file_type} {file_path} permission are {current_value} should be {expected_value}\n",
        )

    @unittest.mock.patch("pathlib.Path.is_file")
    @unittest.mock.patch("pathlib.Path.is_dir")
    @unittest.mock.patch("pathlib.Path.is_socket")
    @unittest.mock.patch("pathlib.Path.is_symlink")
    def test_get_file_type(
        self, mock_is_symlink, mock_is_socket, mock_is_dir, mock_is_file
    ):
        filename = "nonexistent_filename"

        # directory
        mock_is_dir.return_value = True
        self.assertEqual(utils.files.get_file_type(filename), "directory")
        mock_is_dir.return_value = False

        # socket
        mock_is_socket.return_value = True
        self.assertEqual(utils.files.get_file_type(filename), "socket")
        mock_is_socket.return_value = False

        # valid symlink
        mock_is_file.return_value = True
        mock_is_symlink.return_value = True
        self.assertEqual(utils.files.get_file_type(filename), "symlink to file")

        # invalid symlink
        mock_is_file.return_value = False
        mock_is_symlink.return_value = True
        self.assertEqual(utils.files.get_file_type(filename), "broken symlink")

    @unittest.mock.patch("os.stat")
    def test_get_permissions(self, mock_os_stat):
        filename = "nonexistent_filename"

        mock_os_stat.return_value.st_mode = 0o755
        self.assertEqual(utils.files.get_permissions(filename), "755")

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_exit_application(self, mock_stdout):
        # exit 0
        utils.exit.exit_status = 0
        with self.assertRaises(SystemExit) as exit_test:
            utils.exit_application()
        self.assertEqual(exit_test.exception.code, 0)
        self.assertEqual(mock_stdout.getvalue(), "Success\n")

        # reset output
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        # exit errno.EACCES
        utils.exit.set_exit_status(errno.EACCES)
        with self.assertRaises(SystemExit) as exit_test:
            utils.exit_application()
        self.assertEqual(exit_test.exception.code, errno.EACCES)
        self.assertEqual(mock_stdout.getvalue(), "Failed\n")

    def test_load_permissions_definition(self):
        yaml_file = "tests/test/permissions_definition.yaml"
        utils.load_permissions_definition(yaml_file)

        permissions_definition_object = utils.definition.get_permissions_definition()

        self.assertIn("ssh-clippie", permissions_definition_object)
        self.assertIn("main_directory", permissions_definition_object["ssh-clippie"])
        main_directory_object = {
            "condition": "mandatory",
            "type": "directory",
            "mode": "700",
            "description": "SSH client configuration directory",
            "file_types": ["private_key", "public_key"],
        }
        self.assertDictEqual(
            permissions_definition_object["ssh-clippie"]["main_directory"],
            main_directory_object,
        )

        self.assertIn(
            "files",
            permissions_definition_object["ssh-clippie"],
        )
        file_object = {
            "name": "known_hosts",
            "condition": "optional",
            "type": "file",
            "mode": "600",
            "description": "list of host keys known to the user",
        }
        self.assertDictEqual(
            utils.definition.permissions_definition_get_file("known_hosts"), file_object
        )
        self.assertDictEqual(
            utils.definition.permissions_definition_get_file("nonexistent"), {}
        )
        self.assertIn("types", permissions_definition_object["ssh-clippie"])

        type_object = {
            "name": "OpenSSH private key",
            "pattern": ".* private key$",
            "mode": "600",
        }
        self.assertDictEqual(
            utils.definition.permissions_definition_get_file_type("private_key"),
            type_object,
        )

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_display_file_types(self, mock_stdout):
        yaml_file = "tests/test/permissions_definition.yaml"
        utils.load_permissions_definition(yaml_file)

        private_key = utils.definition.display_file_types(
            utils.definition.permissions_definition["ssh-clippie"]["main_directory"][
                "file_types"
            ]
        )
        self.assertIn(
            "and can contain OpenSSH private key, OpenSSH public key",
            mock_stdout.getvalue(),
        )

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_explain(self, mock_stdout):
        yaml_file = "tests/test/permissions_definition.yaml"
        utils.load_permissions_definition(yaml_file)

        utils.explain()

        self.assertIn(
            "Main directory should have permissions set to 700 and can contain OpenSSH private key, OpenSSH public key",
            mock_stdout.getvalue(),
        )
        self.assertIn(
            "known_hosts (list of host keys known to the user) file which is optional and should have permissions set to 600",
            mock_stdout.getvalue(),
        )
        self.assertIn(
            'OpenSSH private key matching file type ".* private key$" should have permissions set to 600',
            mock_stdout.getvalue(),
        )

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_check_permissions(self, mock_stdout):
        yaml_file = "tests/test/permissions_definition.yaml"
        utils.load_permissions_definition(yaml_file)

        utils.set_ssh_directory("tests/test/ssh")

        utils.check_permissions()

        self.assertIn(
            "Checking tests/test/ssh directory",
            mock_stdout.getvalue(),
        )

        self.assertIn(
            "Main directory tests/test/ssh permission are 777 should be 700",
            mock_stdout.getvalue(),
        )

        self.assertIn(
            "file tests/test/ssh/config does not exist",
            mock_stdout.getvalue(),
        )

        self.assertIn(
            "directory tests/test/ssh/config.d permission are 777 should be 700",
            mock_stdout.getvalue(),
        )

        self.assertIn(
            "file tests/test/ssh/config.d/unexpected_file (empty) should not exists",
            mock_stdout.getvalue(),
        )

        self.assertIn(
            "file tests/test/ssh/known_hosts2 should not exist",
            mock_stdout.getvalue(),
        )
