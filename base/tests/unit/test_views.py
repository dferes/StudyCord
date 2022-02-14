from django.test import TestCase
from django.test import Client
from ..testing_utilities import populate_test_db


class UserViewsTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        populate_test_db()
    
    def login_client_user(self, email, password):
        data = {'email': email, 'password': password}
        res = self.client.post(path='/login/', data= data, follow_redirects=True)
        print('RES: ', res.content)
        return self

    def logout_client_user(self):
        '''
        Do I need this???
        '''
        res = self.client.post(path='/logout/', data= {}, follow_redirects=True)
        return self
        
    def tearDown(self):
        pass
        # print('***** UserViewsTests TearDown *****')
        
    def test_home_view(self):
        res = self.client.get('/')
        #print(help(res))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Study Room', str(res.content))
        self.assertIn('Python', str(res.content))
        self.assertIn('Recent Activities', str(res.content))
                
    def test_login_get_view_when_logged_out(self):
        res = self.client.get('/login/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Login', str(res.content))
        self.assertIn('Email', str(res.content))
        self.assertIn('Password', str(res.content))
        self.assertIn("Haven\\\'t signed up yet?", str(res.content))
    
    
    
    def test_login_get_view_when_logged_in(self):
        self.login_client_user(email='testuser@email.com', password='password_123')
        res = self.client.get('/login/')
        self.assertEqual(res.status_code, 302)
        # self.assertIn('', str(res.content))
        print(res.content)
        self.logout_client_user()
    
    def test_register_get_view(self):
        res = self.client.get('/register/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Register', str(res.content))
        self.assertIn('Name', str(res.content))
        self.assertIn('Username', str(res.content))
        self.assertIn('Email', str(res.content))
        self.assertIn('Password', str(res.content))
        self.assertIn('Already signed up?', str(res.content))
        
