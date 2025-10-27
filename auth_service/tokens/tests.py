from django.test import TestCase
import tokens.views as tokens_view

# Create your tests here.

class tokens_view_test(TestCase):
    def setUp(self):
        pass
    
    def test_tokens_test(self):
        acc, ref = tokens_view.create_new_tokens() #make and set in cache
        
        self.assertNotEqual(acc, None, "access should not be None")
        self.assertNotEqual(ref, None, "reference should not be None")
        
        res = tokens_view.is_token_valid(ref) # should not be valid
        self.assertEqual(res, True, "At first token validation should be True")
        
        res = tokens_view.is_in_refresh_token(ref)
        self.assertEqual(res, True, "token should be in the refresh cache")
        
        res = tokens_view.add_token_to_blacklist(ref)
        res = tokens_view.is_token_valid(ref)
        self.assertEqual(res, False, "after add this token in the black list, it should be False")
        
        res = tokens_view.delete_token_from_cache(ref)
        res = tokens_view.is_in_refresh_token(ref)
        self.assertEqual(res, False, "token should not be in the refresh cache")
        
        res = tokens_view.delete_token_from_cache(f'blacklist_{ref}')
        res = tokens_view.is_token_valid(ref) #이 token은 블랙리스트에 없기 때문에 쓸 수 있는 Token이어야한다 --> True
        self.assertEqual(res, True, "after delete, token validation should be False")
        
        