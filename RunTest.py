import unittest
from aiounittest import async_test
from test.TestDBProxy import TestDbProxy

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(TestDbProxy('test_database_setup'))
    #suite.addTest(TestDbProxy('test_clear_hash'))
    #suite.addTest(TestDbProxy('test_should_update'))
    #suite.addTest(TestDbProxy('test_update_hash'))
    #suite.addTest(TestDbProxy('test_fetch_database'))
    #suite.addTest(TestDbProxy('test_split_up_json_cards'))
    #suite.addTest(TestDbProxy('test_save_database'))
    #suite.addTest(TestDbProxy('test_compress_save_card_image'))
    #suite.addTest(TestDbProxy('test_download_one_card_image'))
    #suite.addTest(TestDbProxy('test_download_card_images'))
    #suite.addTest(TestDbProxy('test_decrement_date'))
    #suite.addTest(TestDbProxy('test_complete_url'))
    #suite.addTest(TestDbProxy('test_find_rules_url'))
    #suite.addTest(TestDbProxy('test_update_rules'))
    #suite.addTest(TestDbProxy('test_update_db'))
    # last one isn't really necessary
    #suite.addTest(TestDbProxy('test_loop_check_and_update'))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())