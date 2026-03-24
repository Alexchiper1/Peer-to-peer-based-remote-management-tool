import os
import shutil
import tempfile
import unittest
import s

class TestServer(unittest.TestCase):
    def setUp(self):
        self.old_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)
        s.myFriends.clear()
        s.serverNumber = "1"
        s.portNumber = "5001"

    def tearDown(self):
        os.chdir(self.old_dir)
        shutil.rmtree(self.test_dir)

    def test_make_folder(self):
        result = s.make_folder("demo")
        self.assertIn("folder created", str(result))
        self.assertTrue(os.path.exists("demo"))

    def test_delete_folder(self):
        os.makedirs("gone")
        result = s.delete_folder("gone")
        self.assertIn("folder deleted", str(result))
        self.assertFalse(os.path.exists("gone"))

    def test_delete_folder_not_found(self):
        result = s.delete_folder("missing")
        self.assertIn("folder not found", str(result))

    def test_whoareyou(self):
        result = s.whoareyou()
        self.assertIn("server 1", str(result))
        self.assertIn("5001", str(result))

    def test_get_version(self):
        result = s.get_version()
        self.assertIn(".", str(result))

    def test_ping(self):
        result = s.ping()
        self.assertIn("pong", str(result))

    def test_search_found(self):
        with open("a.txt", "w") as f:
            f.write("hello")
        result = s.search("a.txt")
        self.assertIn("a.txt found", str(result))

    def test_search_not_found(self):
        result = s.search("missing.txt")
        self.assertIn("missing.txt not found", str(result))

    def test_list_friends(self):
        s.myFriends.append("5002")
        s.myFriends.append("5003")
        result = s.list_friends()
        self.assertIn("5002", str(result))
        self.assertIn("5003", str(result))

    def test_online(self):
        result = s.online("5002")
        self.assertIn("5002", s.myFriends)
        self.assertIn("online", str(result))

    def test_offline(self):
        s.myFriends.append("5002")
        result = s.offline("5002")
        self.assertNotIn("5002", s.myFriends)
        self.assertIn("offline", str(result))

    def test_add_friend(self):
        result = s.add_friend("5002")
        self.assertIn("5002", s.myFriends)
        self.assertIn("friend added", str(result))

    def test_remove_friend(self):
        s.myFriends.append("5002")
        result = s.remove_friend("5002")
        self.assertNotIn("5002", s.myFriends)
        self.assertIn("friend removed", str(result))

    def test_pass_message_to_self(self):
        result = s.pass_message("hello", "1")
        self.assertIn("message received: hello", str(result))

if __name__ == "__main__":
    unittest.main()